import os, uuid
from flask import Flask, send_from_directory, request, jsonify, send_file, Response
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
# from app.static.image_processing.image_processing import predict
import mysql.connector
import requests
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app)

url = 'https://earthrover.azurewebsites.net'
# Constants
IMG_SIZE = 256

azure_storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=earthroverdb;AccountKey=rfNYUi7xOR1Gq/8pCEqVyqDkvx8VT2yOxM5yeBqd3AEbJw+zn1dImI1dB3jz5M3ILHbDQS85cFZt+ASt5pjkQw==;EndpointSuffix=core.windows.net"
container_name = "photos"
blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)

model_filename = 'model_34.h5'

class_names = ['Arsura: Burn',
'Carenta de Azot: Nitrogen Deficiency',
'Carenta de Potasiu: Potassium Deficiency',
'Carența de Calciu: Calcium Deficiency',
'Fitotoxicitate: Phytotoxicity',
'Sanatoasa: Healthy']

# Define the predict function
def predict(image_path, model):
    loaded_model = tf.keras.models.load_model(model)
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.expand_dims(image_array, 0)  # Add batch dimension

    # Make predictions
    predictions = loaded_model.predict(image_array)

    # Decode the predictions and return the result
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])  # Get the confidence score
    return predicted_class, confidence

def upload_image_to_blob_storage(image_data, filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(image_data)

def get_image_from_blob_storage(filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_data = blob_client.download_blob()
    image_bytes = blob_data.readall() 
    return image_bytes

def update_image_to_blob_storage(image_data, filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(image_data, overwrite=True)    

def delete_image_from_blob_storage(filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.delete_blob()

def get_model_from_blob_storage(filename):
    blob_client = blob_service_client.get_blob_client(container='model', blob=filename)
    blob_data = blob_client.download_blob()
    model = blob_data.readall()
    return model    

def get_mysql_connection():
    return mysql.connector.connect(
        user="lrronidfvb",
        password="EUKQZVK7XG5B63M4$",
        host="earthrover-server.mysql.database.azure.com",
        port=3306,
        database="earthrover-database",
        ssl_disabled=False
    )

@app.route('/')
def index():
  return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
  return send_from_directory('static', 'favicon.ico')

@app.route('/<path:filename>.js')
def serve_js(filename):
    return send_from_directory('static', f'{filename}.js', mimetype='text/javascript')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        image_file = request.files['image']
        image_data = image_file.read()
        filename = image_file.filename
        image_to_process = image_file
        try:
            model = requests.get(url + '/model/' + model_filename)
        except Exception as e:
            return jsonify({"error1": str(e)}), 500    
        label, confidence = predict(image_to_process, model)

        try:
            upload_image_to_blob_storage(image_data, filename)
        except Exception as e:
            return jsonify({"error2": str(e)}), 500    
        insert_data_url = "{url}/insert_data"
        data = {
            "filename": filename,
            "label": label,
            "confidence": confidence
        }
        try:
            response = requests.post(insert_data_url, json=data)
        except Exception as e:
            return jsonify({"error3": str(e)}), 500    

        
        return jsonify({"message": "Image uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    try:
        image_bytes = get_image_from_blob_storage(filename)
        return Response(image_bytes, mimetype='image/jpg')
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/update_image/<filename>', methods=['PUT'])
def update_image(filename):
    try:
        image_file = request.files['image']
        image_data = image_file.read()
        update_image_to_blob_storage(image_data, filename) 
        return jsonify({"message": "Image updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_image/<filename>', methods=['DELETE'])
def delete_image(filename):
    try:
        delete_image_from_blob_storage(filename)
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        filename = data['filename']
        label = data['label']
        confidence = data['confidence']

        try:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
            blob_client.get_blob_properties()
        except ResourceNotFoundError:
            return jsonify({"error": "File not found in Azure Blob Storage"}), 404
        
        cnx = get_mysql_connection()
        cursor = cnx.cursor()
        cursor.execute('''
            INSERT INTO tomato (filename, label, confidence)
            VALUES (%s, %s, %s)
        ''', (filename, label, confidence))
        cnx.commit()
        cursor.close()
        cnx.close()

        return jsonify({"message": "Data inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
       
@app.route('/model/<filename>', methods=['GET'])    
def get_model(filename):
    try:
        model = get_model_from_blob_storage(filename)
        return Response(model)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    
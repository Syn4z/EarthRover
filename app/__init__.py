import os, uuid
from flask import Flask, render_template, request, jsonify, send_file, Response
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from app.image_processing.image_processing import predict
import mysql.connector
import requests

app = Flask(__name__)
CORS(app)

url = https://earthrover.azurewebsites.net

cnx = mysql.connector.connect(
    user="lrronidfvb",
    password="EUKQZVK7XG5B63M4$",
    host="earthrover-server.mysql.database.azure.com",
    port=3306,
    database="earthrover-database",
    ssl_disabled=False
)
cursor = cnx.cursor()

azure_storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=earthroverdb;AccountKey=rfNYUi7xOR1Gq/8pCEqVyqDkvx8VT2yOxM5yeBqd3AEbJw+zn1dImI1dB3jz5M3ILHbDQS85cFZt+ASt5pjkQw==;EndpointSuffix=core.windows.net"
container_name = "photos"
blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        image_file = request.files['image']
        image_data = image_file.read()
        filename = image_file.filename
        image_to_process = image_file
        label, confidence = predict(image_to_process)

        insert_data_url = "{url}/insert_data"  # Change this to match your endpoint URL
        data = {
            "filename": filename,
            "label": label,
            "confidence": confidence
        }
        response = requests.post(insert_data_url, json=data)

        upload_image_to_blob_storage(image_data, filename)
        
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

        cursor.execute('''
            INSERT INTO tomato (filename, label, confidence)
            VALUES (%s, %s, %s)
        ''', (filename, label, confidence))
        cnx.commit()

        return jsonify({"message": "Data inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
       
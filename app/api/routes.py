from flask import Flask, request
from flask_restful import Resource
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential


connection_string = "DefaultEndpointsProtocol=https;AccountName=earthroverdb;AccountKey=rfNYUi7xOR1Gq/8pCEqVyqDkvx8VT2yOxM5yeBqd3AEbJw+zn1dImI1dB3jz5M3ILHbDQS85cFZt+ASt5pjkQw==;EndpointSuffix=core.windows.net"
container_name = str(uuid.uuid4())

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_service_client.create_container(container_name)

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=image.filename)
    blob_client.upload_blob(image)

    return 'Image uploaded successfully'

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    image_data = blob_client.download_blob().readall()

    return image_data, 200, {'Content-Type': 'image/jpeg'}

@app.route('/image/<filename>', methods=['DELETE'])
def delete_image(filename):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.delete_blob()

    return 'Image deleted successfully'

@app.route('/image/<filename>', methods=['PUT'])
def update_image(filename):
    image = request.files['image']
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(image, overwrite=True)

    return 'Image updated successfully'
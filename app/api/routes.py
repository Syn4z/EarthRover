from flask import Flask, request
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential

# app = Flask(__name__)

# # Azure Blob Storage credentials
# connection_string = "DefaultEndpointsProtocol=https;AccountName=earthroverdb;AccountKey=rfNYUi7xOR1Gq/8pCEqVyqDkvx8VT2yOxM5yeBqd3AEbJw+zn1dImI1dB3jz5M3ILHbDQS85cFZt+ASt5pjkQw==;EndpointSuffix=core.windows.net"
# container_name = str(uuid.uuid4())

# # Create a BlobServiceClient object
# blob_service_client = BlobServiceClient.from_connection_string(connection_string)
# blob_service_client.create_container(container_name)

# # Create a route to handle image uploads
# @app.route('/upload', methods=['POST'])
# def upload_image():
#     # Get the uploaded image file
#     image = request.files['image']

#     # Create a BlobClient object
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=image.filename)

#     # Upload the image to Azure Blob Storage
#     blob_client.upload_blob(image)

#     return 'Image uploaded successfully'

# # Create a route to handle image retrieval
# @app.route('/image/<filename>', methods=['GET'])
# def get_image(filename):
#     # Create a BlobClient object
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

#     # Download the image from Azure Blob Storage
#     image_data = blob_client.download_blob().readall()

#     # Return the image data
#     return image_data, 200, {'Content-Type': 'image/jpeg'}

# # Create a route to handle image deletion
# @app.route('/image/<filename>', methods=['DELETE'])
# def delete_image(filename):
#     # Create a BlobClient object
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

#     # Delete the image from Azure Blob Storage
#     blob_client.delete_blob()

#     return 'Image deleted successfully'

# # Create a route to handle image update
# @app.route('/image/<filename>', methods=['PUT'])
# def update_image(filename):
#     # Get the updated image file
#     image = request.files['image']

#     # Create a BlobClient object
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

#     # Upload the updated image to Azure Blob Storage
#     blob_client.upload_blob(image, overwrite=True)

#     return 'Image updated successfully'
from flask import Flask, Response, request, redirect, url_for, send_file
import subprocess
from datetime import datetime
import time
import io
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

photo_process = None 

def capture_image():
    global photo_process
    
    try:
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        output_filename = f"photos/{timestamp}.jpg"
        subprocess.run(["rpicam-jpeg", "-o", output_filename, "-t", "1", "--width", "2592", "--height", "1944", "--quality", "90"])
        
        return output_filename
    except Exception as e:
        return None

def send_photo_to_server(photo_file):
    url = 'http://192.168.189.190:5000/image'
    
    try:
        files = {'image': open(photo_file, 'rb')}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("Photo uploaded successfully!")
        else:
            print("Failed to upload photo. Status code:", response.status_code)
    except Exception as e:
        print("Error uploading photo:", e)

@app.route('/video_feed', methods=['GET'])
def capture_photo():
    global photo_process
    
    if photo_process:
        photo_process.terminate()
    
    try:
        command = ["rpicam-jpeg", "-o", '/dev/stdout', "-t", "1000", "--width", "2592", "--height", "1944", "--quality", "90", "--nopreview"]
        photo_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = photo_process.communicate()

        if photo_process.returncode != 0:
            return f"Error: {error.decode('utf-8')}"
        image_data = io.BytesIO(output)
        return send_file(image_data, mimetype='image/jpeg')

    except Exception as e:
        return str(e)

@app.route('/take_photo', methods=['POST'])
def take_photo():
    global photo_process
    
    if photo_process: 
        photo_process.terminate()
    
    output_file = capture_image()
    if output_file:
        print(f"Image captured and saved as {output_file}")
        send_photo_to_server(output_file)
        return "Photo captured successfully!"
    else:
        return "Failed to capture photo."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

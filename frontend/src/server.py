from flask import Flask, request, send_file
from flask_cors import CORS
from datetime import datetime
import json
import os
import base64

app = Flask(__name__)
CORS(app)

@app.route('/video_feed', methods=['GET'])
def live():
  # Check if the image is available
  try:
    return send_file('./assets/img/live_img.jpg', mimetype='image/jpeg')
  except:
    return 'Image not found', 404

@app.route('/diseases', methods=['GET'])
def diseases():
  with open('./app/data/diseases.json', 'r') as f:
    diseases = json.load(f)
  return json.dumps(diseases)

@app.route('/photo_analysis', methods=['GET'])
def photo_analysis():
  return json.dumps([{
      "name": "Early Blight",
      "confidence": 0.98
    }, {
      "name": "Late Blight",
      "confidence": 0.92
    }, {
      "name": "Healthy",
      "confidence": 0.85
    }, {
      "name": "Septoria Leaf Spot",
      "confidence": 0.75
    },
    {
      "name": "Bacterial Spot",
      "confidence": 0.65
    }
  ])

@app.route('/disease', methods=['POST'])
def add_disease():
  new_disease = request.get_json()

  with open('./app/data/diseases.json', 'r+') as f:
    diseases = json.load(f)
    diseases.insert(0, new_disease)
    f.seek(0)
    json.dump(diseases, f, indent=4)
    f.truncate()

  return 'Disease added', 200

@app.route('/disease', methods=['DELETE'])
def delete_disease():
  # Delete first disease from json 
  with open('./app/data/diseases.json', 'r+') as f:
    diseases = json.load(f)
    diseases.pop(0)
    f.seek(0)
    json.dump(diseases, f, indent=4)
    f.truncate()

  return 'Disease deleted', 200 

@app.route('/image', methods=['POST'])
def add_image():
  results = request.get_json()

  for result in results:
    print(result['filename'])

    # Checx if filename does not exist in assets/img/db
    if not os.path.exists(f'./assets/img/db/{result["filename"]}'):
      # Copy the image from app/photos to assets/img/db
      with open(f'../../app/photos/{result["filename"]}', 'rb') as f:
        with open(f'./assets/img/db/{result["filename"]}', 'wb') as img:
          img.write(f.read())
      
      # Update the diseases.json file
      with open('./app/data/diseases.json', 'r+') as f:
        diseases = json.load(f)
        
        description = "A common disease of many plants. It is caused by a fungus that is spread by water"
        treatment = ["Fungicide", "Remove infected leaves"]

        if result["label"] == "Healthy":
          description = "No disease detected"
          treatment = []

        diseases.append({
          "id": len(diseases) + 1,
          "name": result["label"],
          "description": description,
          "treatment": treatment,
          "confidence": int(result["confidence"]),
          "date": datetime.now().strftime("%B") + ', ' + datetime.now().strftime("%Y"),
          "image": f'./assets/img/db/{result["filename"]}',
          "timestamp": datetime.now().timestamp()
        })

        f.seek(0)
        json.dump(diseases, f, indent=2)
        f.truncate()
  

  return {'All images uploaded': 200}

if __name__ == '__main__':
  app.run(port=7777, debug=True)
from flask import Flask, request, send_file
from flask_cors import CORS

import json

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

if __name__ == '__main__':
  app.run(debug=True)
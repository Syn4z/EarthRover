from flask import Blueprint, request, jsonify
from image_processing.image_processing import predict
from database.database import db
from database.predicted_images import PredictedImages
import os

routes = Blueprint('routes', __name__)
UPLOAD_FOLDER = 'photos'

@routes.route('/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if image.filename in os.listdir(UPLOAD_FOLDER):
        return jsonify({'error': 'File already exists'})
    else:    
        filename = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(filename)
    
    label, confidence = predict(filename)
    new_image = PredictedImages(name=image.filename, label=str(label), confidence=confidence*100)
    db.session.add(new_image)
    db.session.commit()
    
    return jsonify({'message': 'Image uploaded successfully'})

@routes.route('/image/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = PredictedImages.query.get(image_id)
    if image:
        try:
            os.remove(f'{UPLOAD_FOLDER}/{image.name}')
        except FileNotFoundError:
            pass    
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': 'Image deleted successfully'})
    else:
        return jsonify({'error': 'Image not found'})

@routes.route('/image/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    image = PredictedImages.query.get(image_id)
    if image:
        image.label = request.form.get('label', '')
        image.confidence = request.form.get('confidence', '')
        db.session.commit()
        return jsonify({'message': 'Image updated successfully'})
    else:
        return jsonify({'error': 'Image not found'})

@routes.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = PredictedImages.query.get(image_id)
    if image:
        return jsonify({'filename': image.name, 'label': image.label, 'confidence': image.confidence})
    else:
        return jsonify({'error': 'Image not found'})
    
@routes.route('/image', methods=['GET'])
def get_all_images():
    images = PredictedImages.query.all()
    image_list = []
    for image in images:
        image_data = {
            'filename': image.name,
            'label': image.label,
            'confidence': image.confidence
        }
        image_list.append(image_data)
    return jsonify({'images': image_list})    

from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import os

routes = Blueprint('routes', __name__)
mysql = MySQL()

UPLOAD_FOLDER = 'photos'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@routes.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to image processing API'})

@routes.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'})
    
    filename = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filename)
    
    # # Get label and confidence from request
    # label = request.form.get('label', '')
    # confidence = request.form.get('confidence', '')
    
    # # Insert metadata into MySQL database
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO images (filename, label, confidence) VALUES (%s, %s, %s)", (filename, label, confidence))
    # mysql.connection.commit()
    # cur.close()
    
    return jsonify({'message': 'Image uploaded successfully'})

@routes.route('/delete/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT filename FROM images WHERE id = %s", (image_id,))
    data = cur.fetchone()
    if data:
        filename = data[0]
        os.remove(filename)
        cur.execute("DELETE FROM images WHERE id = %s", (image_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Image deleted successfully'})
    else:
        cur.close()
        return jsonify({'error': 'Image not found'})

@routes.route('/update/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    label = request.form.get('label')
    confidence = request.form.get('confidence')
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE images SET label = %s, confidence = %s WHERE id = %s", (label, confidence, image_id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'Image updated successfully'})

@routes.route('/get/<int:image_id>', methods=['GET'])
def get_image(image_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT filename, label, confidence FROM images WHERE id = %s", (image_id,))
    data = cur.fetchone()
    cur.close()
    if data:
        filename, label, confidence = data
        return jsonify({'filename': filename, 'label': label, 'confidence': confidence})
    else:
        return jsonify({'error': 'Image not found'})

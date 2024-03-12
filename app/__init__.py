from flask import Flask, render_template
from flask_restful import Api
from .api.routes import upload_image, get_image, delete_image, update_image

app = Flask(__name__)
api = Api(app, prefix='/api')
api.add_resource(upload_image, '/upload')

@app.route('/')
def index():
    return render_template('index.html')

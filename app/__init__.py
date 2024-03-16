from flask import Flask, render_template
# from flask_restful import Api
# from .api.routes import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# api = Api(app, prefix='/api')
# api.add_resource(upload_image, '/upload')
# api.add_resource(get_image, '/image/<filename>')
# api.add_resource(delete_image, '/image/<filename>')
# api.add_resource(update_image, '/image/<filename>')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def upload():
    return {"This": "works"}

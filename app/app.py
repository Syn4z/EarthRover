from flask import Flask
from routes import routes
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'image_db'

mysql = MySQL(app)
mysql.init_app(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='192.168.189.190', port=5000, debug=True)

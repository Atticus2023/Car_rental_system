from flask import Flask
from .views.auth import auth
from .views.routes import routes
from .db import mysql
import re
import bcrypt

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(routes)

app.secret_key = "car_rental_system"

# Database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lincoln2023'
app.config['MYSQL_DB'] = 'car_rental_system'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql.init_app(app)

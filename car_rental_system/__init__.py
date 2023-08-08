from flask import Flask

from flask_mysqldb import MySQL
# from .db import mysql
import re
import bcrypt
mysql = MySQL()

def creat_app():
    app = Flask(__name__)

    app.secret_key = "car_rental_system"
    
    # Database connection details below
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'lincoln2023'
    app.config['MYSQL_DB'] = 'car_rental_system'
    app.config['MYSQL_PORT'] = 3306
    mysql.init_app(app)
    from .views.auth import auth
    from .views.routes import routes
    app.register_blueprint(auth)
    app.register_blueprint(routes)
    # Intialize MySQL
    return app

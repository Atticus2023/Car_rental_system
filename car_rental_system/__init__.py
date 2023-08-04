from flask import Flask

app = Flask(__name__)

from car_rental_system.views import auth, routes
from flask import render_template, redirect, request, url_for, session, flash
from car_rental_system import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt

@app.route("/car")
def car():
    return "car"
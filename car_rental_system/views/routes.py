from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from car_rental_system.db import mysql
import MySQLdb.cursors
import re
import bcrypt

routes = Blueprint('routes', __name__)

@routes.route("/user_details")
def user_details():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    # Check user type
    if session.get('user_type') == "staff" or session.get('user_type') == "admin":
        cursor.execute('SELECT * FROM staffs WHERE user_ID = %s', (session.get('user_ID'),))
        user_details = cursor.fetchone()
        cursor.close()
       
    elif session.get('user_type') == "customer":
        cursor.execute('SELECT * FROM customers WHERE user_ID = %s', (session.get('user_ID'),))
        user_details = cursor.fetchone()
        cursor.close()
    print(user_details)
    return render_template("user_details.html", user_details=user_details, user_ID = session.get('user_ID'), username = session.get('username'), email = session.get('email'), user_type = session.get('user_type'))

@routes.route("/car_list")
def car_list():
    user_type = session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    print(user_type)
    return render_template("car_list.html", cars=cars, user_type=user_type)

@routes.route("/staff_list")
def staff_list():
    pass

@routes.route("/customer_list")
def customer_list():
    pass

@routes.route("/update_profile")
def update_profile():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    
    user_ID = session.get('user_ID')
    username = session.get('username')
    user_type = session.get('user_type')
    email = session.get('email')
    cursor = mysql.connection.cursor()
    if user_type == "staff" or user_type == "admin":
        cursor.execute('SELECT * FROM staffs WHERE user_ID = %s', (user_ID,))
        user_details = cursor.fetchone()
        cursor.close()       
    elif user_type == "customer":
        cursor.execute('SELECT * FROM customers WHERE user_ID = %s', (user_ID,))
        user_details = cursor.fetchone()
        
    if request.method == 'POST':
        new_username = request.form.get("new_username")
        new_password = request.form.get("new_password")
        new_user_first_name = request.form.get("new_user_first_name")
        new_user_last_name = request.form.get("new_user_last_name")
        new_user_address = request.form.get("new_user_address")
        new_email = request.form.get("new_email")
        new_user_phone_number = request.form.get("new_user_phone_number")

        cursor.execute('UPDATE users SET username=%s WHERE user_ID=%s', (new_username, user_ID))

        if new_password:
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('UPDATE users SET new_password=%s WHERE user_ID=%s', (hashed, user_ID))
        
        
        if user_type == "staff" or user_type == "admin":
            cursor.execute('UPDATE staffs SET staff_first_name=%s, staff_last_name=%s, staff_address=%s, staff_email=%s, staff_phone_number=%s WHERE user_ID=%s', (new_user_first_name, new_user_last_name, new_user_address, new_email, new_user_phone_number, user_ID))
        
        elif user_type == "customer":
            cursor.execute('UPDATE customers SET customer_first_name=%s, customer_last_name=%s, customer_address=%s, customer_email=%s, customer_phone_number=%s WHERE user_ID=%s', (new_user_first_name, new_user_last_name, new_user_address, new_email, new_user_phone_number, user_ID))
        mysql.connection.commit()
        cursor.close() 
        # cursor.execute('SELECT * FROM customers WHERE user_ID = %s', (user_ID,))
        # customer_details = cursor.fetchone()
    return render_template("update_profile.html", user_details = user_details, username = username, email = email)


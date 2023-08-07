from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from car_rental_system.db import mysql
import MySQLdb.cursors
import re
import bcrypt
from datetime import datetime
from functools import wraps

routes = Blueprint('routes', __name__)


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'admin':
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_function

def staff_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'admin' and session.get('user_type') != 'staff':
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_function

@routes.route("/user_details")
def user_details():
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    user_type=session.get('user_type')
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
    
    return render_template("user_details.html", user_details=user_details, user_ID = session.get('user_ID'), username = session.get('username'), email = session.get('email'), user_type = session.get('user_type'))


@routes.route("/update_profile", methods=['GET', 'POST'])
def update_profile():
    msg = ''
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    
    user_ID = session.get('user_ID')
    username = session.get('username')
    user_type = session.get('user_type')
    email = session.get('email')
    cursor = mysql.connection.cursor()
    if user_type == "staff" or user_type == "admin":
        cursor.execute('SELECT * FROM staffs WHERE user_ID = %s', (user_ID,))
        user_details = cursor.fetchone()
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

        cursor.execute('SELECT username FROM users WHERE user_ID <> %s', (user_ID,))
        usernames = cursor.fetchall()
        if new_username in usernames:
            msg = 'This username already exists!'
        elif len(new_username) > 50:
            msg = 'Username is too long!'
        elif not re.match(r'[A-Za-z0-9]+', new_username):
            msg = 'Username must contain only characters and numbers!'
        elif len(new_user_first_name) > 50 or len(new_user_last_name) > 50 :
            msg = 'Name too long!'
        elif not re.match(r'^[a-zA-Z]+$', new_user_first_name) or re.match(r'^[a-zA-Z]+$', new_user_last_name):
            msg = 'Name not just letters!'
        elif len(new_user_address) > 250:
            msg = 'Adress is too long!'
        elif len(new_email) > 50:
            msg = 'Email address is too long!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', new_email):
            msg = 'Invalid email address!'
        elif len(new_user_phone_number) > 20:
            msg = 'Phone number is too long!'
        elif not re.match(r'^\d+$', new_user_phone_number):
            msg = 'Invalid phone number!'
        else:
            cursor.execute('UPDATE users SET username=%s, email=%s WHERE user_ID=%s', (new_username, new_email, user_ID))
            mysql.connection.commit()

        if new_password:
            if len(new_password) < 6 or len(new_password) > 20:
                msg = 'Password must be between 6 and 20 characters!'
        # Check is there any space in password
            elif re.search(r'\s', new_password):
                msg = 'Password cannot contain spaces!'
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('UPDATE users SET new_password=%s WHERE user_ID=%s', (hashed, user_ID))
            mysql.connection.commit()
                
        if user_type == "staff" or user_type == "admin":
            cursor.execute('UPDATE staffs SET staff_first_name=%s, staff_last_name=%s, staff_address=%s, staff_phone_number=%s WHERE user_ID=%s', (new_user_first_name, new_user_last_name, new_user_address, new_user_phone_number, user_ID))
            mysql.connection.commit()
            cursor.close() 
            return redirect(url_for('routes.user_details'))
        
        elif user_type == "customer":
            cursor.execute('UPDATE customers SET customer_first_name=%s, customer_last_name=%s, customer_address=%s, customer_phone_number=%s WHERE user_ID=%s', (new_user_first_name, new_user_last_name, new_user_address, new_user_phone_number, user_ID))
            mysql.connection.commit()
            cursor.close() 
            return redirect(url_for('routes.user_details'))
    return render_template("update_profile.html", user_details = user_details, username = username, email = email, user_type=user_type,msg=msg)

@routes.route("/car_list")
def car_list():
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    
    user_type = session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    print(cars)
    cursor.close()
    return render_template("car_list.html", cars=cars, user_type=user_type)

@routes.route("/car_details/<int:car_ID>")
def car_details(car_ID):
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    user_type = session.get('user_type')
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cars WHERE car_ID=%s', (car_ID,))
    car_details=cursor.fetchone()
    cursor.close()
    return render_template("car_details.html", car_details=car_details,user_type=user_type)

@routes.route("/car_add", methods=['GET', 'POST'])
@staff_required
def car_add():
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    user_type=session.get('user_type')
    msg=''
    if request.method == 'POST':
        license_plate = request.form.get('license_plate')
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        seating_capacity = request.form.get('seating_capacity')
        price_per_day = request.form.get('price_per_day')
        transmission = request.form.get('transmission')
        current_year = datetime.now().year        
        print(seating_capacity)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT license_plate FROM cars')
        license_plates = cursor.fetchall()
        if license_plate in license_plates:
            msg = 'This license_plate already exists!'
        elif len(license_plate) > 15:
            msg = 'License_plate is too long!'
        elif not re.match(r'[A-Za-z0-9]+', license_plate):
            msg = 'License_plate must contain only characters and numbers!'
        elif len(make) > 50 :
            msg = 'Make too long!'
        elif len(model) > 50:
            msg = 'Model is too long!'
        elif  not re.match(r'^\d{4}$', year) or int(year) > current_year:
            msg = 'Year is wrong!'
        elif not re.match(r'^[1-9]\d*$', seating_capacity) :
            msg = 'Seating capacity is wrong!'
        elif not re.match(r'^\d+(\.\d+)?$', price_per_day):
            msg = 'Invalid price!'
        elif float(price_per_day)<0:
            msg = 'Invalid price!'
        else:            
            cursor.execute('INSERT INTO cars (license_plate, make, model, year, seating_capacity, price_per_day, transmission) VALUES (%s, %s, %s, %s, %s, %s, %s)', (license_plate,make,model,year,seating_capacity,price_per_day,transmission))
            mysql.connection.commit()
            cursor.close() 
            return redirect(url_for('routes.car_list'))
    return render_template("car_add.html", user_type=user_type, msg=msg)

@routes.route("/car_edit/<int:car_ID>", methods=['GET', 'POST'])
@staff_required
def car_edit(car_ID):
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    
    user_type=session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM cars WHERE car_ID=%s', (car_ID,))
    car_details=cursor.fetchone()

    if request.method == 'POST':
        new_license_plate = request.form.get('license_plate')
        new_make = request.form.get('make')
        new_model = request.form.get('model')
        new_year = request.form.get('year')
        new_seating_capacity = request.form.get('seating_capacity')
        new_price_per_day = request.form.get('price_per_day')
        new_transmission = request.form.get('transmission')
        current_year = datetime.now().year
        
        cursor.execute('SELECT license_plate FROM cars')
        license_plates = cursor.fetchall()
        if new_license_plate in license_plates:
            msg = 'This license_plate already exists!'
        elif len(new_license_plate) > 15:
            msg = 'License_plate is too long!'
        elif not re.match(r'[A-Za-z0-9]+', new_license_plate):
            msg = 'License_plate must contain only characters and numbers!'
        elif len(new_make) > 50 :
            msg = 'Make too long!'
        elif len(new_model) > 50:
            msg = 'Model is too long!'
        elif  not re.match(r'^\d{4}$', new_year):  
            msg = 'Year is wrong!'
        elif int(new_year) > current_year:
            msg = 'Year is wrong!'
        elif re.match(r'^[1-9]\d*$', new_seating_capacity) :
            msg = 'Seating capacity is wrong!'
        elif not re.match(r'^\d+(\.\d+)?$', new_price_per_day):
            msg = 'Invalid price!'
        elif float(new_price_per_day)<0:
            msg = 'Invalid price!'
        cursor.execute('UPDATE cars SET license_plate=%s, make=%s, model=%s, year=%s, seating_capacity=%s, price_per_day=%s, transmission=%s WHERE car_ID=%s', (new_license_plate,new_make,new_model,new_year,new_seating_capacity,new_price_per_day,new_transmission, car_ID))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('routes.car_list'))
    
    return render_template("car_edit.html", car_details=car_details,user_type=user_type)

@routes.route("/car_delete/<int:car_ID>")
@staff_required
def car_delete(car_ID):
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))
    
    user_type=session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM cars WHERE car_ID=%s', (car_ID,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('routes.car_list'))

@routes.route("/customer_list")
@staff_required
def customer_list():
    user_type=session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT u.user_ID, u.username, u.email, c.customer_first_name, c.customer_last_name, c.customer_address,  c.customer_phone_number FROM users u JOIN customers c ON u.user_ID=c.user_ID')
    customers = cursor.fetchall()
    cursor.close()
    return render_template("customer_list.html", customers=customers, user_type=user_type)

@routes.route("/customer_edit/<int:user_ID>", methods=['GET','POST'])
@admin_required
def customer_edit(user_ID):
    user_type=session.get('user_type')    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT u.user_ID, u.username, u.email, c.customer_first_name, c.customer_last_name, c.customer_address, c.customer_email, c.customer_phone_number FROM users u JOIN customers c ON u.user_ID=c.user_ID WHERE u.user_ID=%s', (user_ID,))
    customer_details=cursor.fetchone()

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_customer_first_name = request.form.get('customer_first_name')
        new_customer_last_name = request.form.get('customer_last_name')
        new_customer_address = request.form.get('customer_address')
        new_customer_email = request.form.get('customer_email')
        new_customer_phone_number = request.form.get('customer_phone_number')

        cursor.execute('SET username FROM users WHERE user_ID <> %s', (user_ID,))
        usernames = cursor.fetchall()

        if new_username in usernames:
            msg = 'This username already exists!'
        elif len(new_username) > 50:
            msg = 'Username is too long!'
        elif not re.match(r'[A-Za-z0-9]+', new_username):
            msg = 'Username must contain only characters and numbers!'
        elif len(new_customer_first_name) > 50 or len(new_customer_last_name) > 50 :
            msg = 'Name too long!'
 
        elif len(new_customer_address) > 250:
            msg = 'Adress is too long!'
        elif len(new_customer_email) > 50:
            msg = 'Email address is too long!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', new_customer_email):
            msg = 'Invalid email address!'
        elif len(new_customer_phone_number) > 20:
            msg = 'Phone number is too long!'
        elif not re.match(r'^\d+$', new_customer_phone_number):
            msg = 'Invalid phone number!'
        else:
            cursor.execute('UPDATE users SET username=%s, email=%s WHERE user_ID=%s', (new_username, new_customer_email,user_ID))
            cursor.execute('UPDATE customers SET customer_first_name=%s, customer_last_name=%s, customer_address=%s, customer_phone_number=%s WHERE user_ID=%s', (new_customer_first_name,new_customer_last_name,new_customer_address,new_customer_phone_number, user_ID))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('routes.customer_list'))
    
    return render_template("customer_edit.html", customer_details=customer_details, user_type=user_type)

@routes.route("/customer_add", methods=['GET', 'POST'])
@admin_required
def customer_add():
    user_type=session.get('user_type')
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif len(username) > 50:
            msg = 'Username is too long!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        elif len(password) < 6 or len(password) > 20:
            msg = 'Password must be between 6 and 20 characters!'
        # Check is there any space in password
        elif re.search(r'\s', password):
            msg = 'Password cannot contain spaces!'
        elif len(email) > 50:
            msg = 'Email address is too long!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO users (username, password, email, user_type) VALUES (%s, %s,%s, %s)', (username, hashed, email, 'customer'))
                mysql.connection.commit()
                #Get the user_ID
                user_ID = cursor.lastrowid
                cursor.execute('INSERT INTO customers (user_ID, customer_first_name, customer_last_name, customer_phone_number ) VALUES (%s, %s, %s, %s)', (user_ID, 'customer', 'customer', '0000000'))
                mysql.connection.commit()
            except Exception as e:
                # Something went wrong, rollback the transaction
                mysql.connection.rollback()
                flash('An error occurred while creating this user.')
                return redirect("routes.customer_list.html")
            finally:
                cursor.close()
            # flash('You have successfully add a customer!'  'success') 
            # Redirect to customer_list page after successful registration
            return redirect("routes.customer_list.html")
    else:
        return render_template('customer_add.html', msg=msg, user_type=user_type)

@routes.route("/customer_delete/<int:user_ID>")
@admin_required
def customer_delete(user_ID):
   
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM users WHERE user_ID=%s', (user_ID,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('routes.customer_list'))

@routes.route("/staff_list")
@admin_required
def staff_list():
    user_type=session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT u.user_ID, u.username, u.email, s.staff_first_name, s.staff_last_name, s.staff_address, s.staff_phone_number FROM users u JOIN staffs s ON u.user_ID=s.user_ID')
    staffs = cursor.fetchall()
    cursor.close()
    return render_template("staff_list.html", staffs=staffs, user_type=user_type)

@routes.route("/staff_edit/<int:user_ID>", methods=['GET','POST'])
@admin_required
def staff_edit(user_ID):    
    user_type=session.get('user_type')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT u.user_ID, u.username, u.email, s.staff_first_name, s.staff_last_name, s.staff_address, s.staff_phone_number FROM users u JOIN staffs s ON u.user_ID=s.user_ID WHERE u.user_ID=%s', (user_ID,))
    staff_details=cursor.fetchone()

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_staff_first_name = request.form.get('new_staff_first_name')
        new_staff_last_name = request.form.get('new_staff_last_name')
        new_staff_address = request.form.get('new_staff_address')
        new_staff_email = request.form.get('new_staff_email')
        new_staff_phone_number = request.form.get('new_staff_phone_number')

        cursor.execute('SET username FROM users WHERE user_ID <> %s', (user_ID,))
        usernames = cursor.fetchall()
        if new_username in usernames:
            msg = 'This username already exists!'
        elif len(new_username) > 50:
            msg = 'Username is too long!'
        elif not re.match(r'[A-Za-z0-9]+', new_username):
            msg = 'Username must contain only characters and numbers!'
        elif len(new_staff_first_name) > 50 or len(new_staff_last_name) > 50 :
            msg = 'Name too long!'
        # elif len(password) < 6 or len(password) > 20:
        #     msg = 'Password must be between 6 and 20 characters!'
        # # Check is there any space in password
        # elif re.search(r'\s', password):
        #     msg = 'Password cannot contain spaces!'
        elif len(new_staff_address) > 250:
            msg = 'Adress is too long!'
        elif len(new_staff_email) > 50:
            msg = 'Email address is too long!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', new_staff_email):
            msg = 'Invalid email address!'
        elif len(new_staff_phone_number) > 20:
            msg = 'Phone number is too long!'
        elif not re.match(r'^\d+$', new_staff_phone_number):
            msg = 'Invalid phone number!'
        else:
            cursor.execute('UPDATE users SET username=%s, email WHERE user_ID=%s', (new_username, new_staff_email, user_ID))
            cursor.execute('UPDATE staffs SET staff_first_name=%s, staff_last_name=%s, staff_address=%s, staff_phone_number=%s WHERE user_ID=%s', (new_staff_first_name,new_staff_last_name,new_staff_address,new_staff_phone_number, user_ID))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('routes.staff_list'))
    
    return render_template("staff_edit.html", staff_details=staff_details,user_type=user_type)


@routes.route("/staff_add", methods=['GET', 'POST'])
@admin_required
def staff_add():
    user_type=session.get('user_type')
    msg = ''    
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif len(username) > 50:
            msg = 'Username is too long!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        elif len(password) < 6 or len(password) > 20:
            msg = 'Password must be between 6 and 20 characters!'
        # Check is there any space in password
        elif re.search(r'\s', password):
            msg = 'Password cannot contain spaces!'
        elif len(email) > 50:
            msg = 'Email address is too long!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO users (username, password, email, user_type) VALUES (%s, %s, %s,%s)', (username, hashed, email, 'staff'))
            mysql.connection.commit()

            user_ID = cursor.lastrowid
            cursor.execute('INSERT INTO staffs (user_ID, staff_first_name, staff_last_name, staff_phone_number) VALUES (%s, %s, %s, %s)', (user_ID, 'Staff', 'Staff', '0000000'))
            mysql.connection.commit()
            cursor.close()
            flash('You have successfully add a staff!'  'success') 
            # Redirect to login page after successful registration
            return redirect(url_for('routes.staff_list'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('staff_add.html', msg=msg, user_type=user_type)

@routes.route("/staff_delete/<int:user_ID>")
@admin_required
def staff_delete(user_ID):
   
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM users WHERE user_ID=%s', (user_ID,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('routes.staff_list'))

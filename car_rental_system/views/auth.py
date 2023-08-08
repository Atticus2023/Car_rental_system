from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from car_rental_system import mysql
import MySQLdb.cursors
import re
import bcrypt

auth = Blueprint('auth', __name__)


@auth.route("/")
def index():
    return render_template("index.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == "POST" and "username" in request.form and "password" in request.form and 'email' in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
       
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif len(email) > 50:
            msg = 'Email address is too long!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif len(username) > 50:
            msg = 'Username is too long!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        elif len(password) < 6 or len(password) > 20:
            msg = 'Password must be between 6 and 20 characters!'
        # Check is there any space in password
        elif re.search(r'\s', password):
            msg = 'Password cannot contain spaces!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Just customer need to register, for staffs, admin add them to mysql
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s,%s)', (username, hashed, email, 'customer'))
            mysql.connection.commit()
            # Get user_ID, then insert to table customer
            user_ID = cursor.lastrowid
            print (user_ID)
            cursor.execute('INSERT INTO customers (user_ID, customer_first_name, customer_last_name, customer_phone_number) VALUES (%s, %s, %s, %s)', (user_ID, 'Customer', 'Customer', '0000000'))
            mysql.connection.commit()
            cursor.close()
            flash('You have successfully registered!')
            return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form.get('username')
        user_password = request.form.get('password')
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cursor.close()
        print(account)
        if account is not None:
            password = account['password']
            if bcrypt.checkpw(user_password.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['user_ID'] = account['user_ID']
                session['username'] = account['username']
                session['user_type'] = account['user_type']
                session['email'] = account['email']
                
                return render_template("base_routes.html", user_type=session['user_type'],username = username)
                # if session['user_type'] == 'admin':
                #     return render_template("admin_dashboard.html", username = username)
                # elif session['user_type'] == 'staff':
                #     return render_template("staff_dashboard.html", username = username)
                # elif session['user_type'] == 'customer':
                #     return render_template("customer_dashboard.html", username = username)
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@auth.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('user_ID', None)
   session.pop('username', None)
   session.pop('user_type', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('auth.login'))



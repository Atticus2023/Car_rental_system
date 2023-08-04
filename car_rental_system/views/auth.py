from flask import render_template, redirect, request, url_for, session, flash
from car_rental_system import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt


app.secret_key = "car_rental_system"

# Database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lincoln2023'
app.config['MYSQL_DB'] = 'car_rental_system'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == "POST" and "username" in request.form and "password" in request.form and 'email' in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        print(username)
        print(password)
        print(email)
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s,%s)', (username, hashed, email, 'admin'))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
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
                if session['user_type'] == 'admin':
                    return render_template("admin_dashboard.html", username = username)
                elif session['user_type'] == 'staff':
                    return render_template("staff_dashboard.html", username = username)
                elif session['user_type'] == 'customer':
                    return render_template("customer_dashboard.html", username = username)
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
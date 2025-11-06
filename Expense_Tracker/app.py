from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
from flask_mysqldb import MySQL # type: ignore
import MySQLdb.cursors # type: ignore
import re
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'omapar00'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'simple_expense_tracker'

mysql = MySQL(app)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        hashed_password = generate_password_hash(password)  # Default hash method
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM app_users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO app_users (username, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    return render_template('signup.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM app_users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account and check_password_hash(account['password'], password):
            session['user_id'] = account['id']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/home', methods=['GET'])
@login_required
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_expenses WHERE user_id = %s', (session['user_id'],))
    expenses = cursor.fetchall()
    return render_template('home.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form.get('description')
        amount = request.form.get('amount')
        date_added = datetime.now().date()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO user_expenses (user_id, description, amount, date_added) VALUES (%s, %s, %s, %s)', (session['user_id'], description, amount, date_added))
        mysql.connection.commit()
        return redirect(url_for('home'))
    return render_template('add_expense.html')

@app.route('/stats', methods=['GET'])
@login_required
def stats():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Total amount per day
    cursor.execute("""
        SELECT DATE(date_added) AS date, SUM(amount) AS total_amount
        FROM user_expenses
        WHERE user_id = %s
        GROUP BY DATE(date_added)
        ORDER BY DATE(date_added) DESC
    """, (session['user_id'],))
    daily_totals = cursor.fetchall()
    
    # Total amount per month
    cursor.execute("""
        SELECT YEAR(date_added) AS year, MONTH(date_added) AS month, SUM(amount) AS total_amount
        FROM user_expenses
        WHERE user_id = %s
        GROUP BY YEAR(date_added), MONTH(date_added)
        ORDER BY YEAR(date_added) DESC, MONTH(date_added) DESC
    """, (session['user_id'],))
    monthly_totals = cursor.fetchall()
    
    # Total amount per year
    cursor.execute("""
        SELECT YEAR(date_added) AS year, SUM(amount) AS total_amount
        FROM user_expenses
        WHERE user_id = %s
        GROUP BY YEAR(date_added)
        ORDER BY YEAR(date_added) DESC
    """, (session['user_id'],))
    yearly_totals = cursor.fetchall()
    
    return render_template('stats.html', daily_totals=daily_totals, monthly_totals=monthly_totals, yearly_totals=yearly_totals)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

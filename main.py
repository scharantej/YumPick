
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize the Flask app
app = Flask(__name__)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Create the Dish model
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    delivery_info = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    votes = db.Column(db.Integer, default=0)

# Create the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)

# Create the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

# Create the database tables
db.create_all()

# Set up the secret key for session management
app.secret_key = os.urandom(24)

# Define the home page route
@app.route('/')
def index():
    # Get the dish of the week
    dish_of_the_week = Dish.query.order_by(Dish.votes.desc()).first()

    # Render the home page
    return render_template('index.html', dish_of_the_week=dish_of_the_week)

# Define the poll page route
@app.route('/poll')
def poll():
    # Get all dishes
    dishes = Dish.query.all()

    # Render the poll page
    return render_template('poll.html', dishes=dishes)

# Define the poll submission route
@app.route('/poll', methods=['POST'])
def poll_submit():
    # Get the selected dish ID
    dish_id = request.form.get('dish_id')

    # Find the dish in the database
    dish = Dish.query.get(dish_id)

    # Increment the dish's vote count
    dish.votes += 1

    # Save the changes to the database
    db.session.commit()

    # Flash a success message
    flash('Your vote has been recorded.')

    # Redirect back to the poll page
    return redirect(url_for('poll'))

# Define the menu page route
@app.route('/menu')
def menu():
    # Get the dish of the week
    dish_of_the_week = Dish.query.order_by(Dish.votes.desc()).first()

    # Render the menu page
    return render_template('menu.html', dish_of_the_week=dish_of_the_week)

# Define the order submission route
@app.route('/order', methods=['POST'])
def order():
    # Get the order details
    dish_id = request.form.get('dish_id')
    quantity = request.form.get('quantity')
    delivery_address = request.form.get('delivery_address')

    # Get the dish from the database
    dish = Dish.query.get(dish_id)

    # Calculate the total cost of the order
    total_cost = dish.cost * int(quantity)

    # Create a new order
    order = Order(
        user_id=session['user_id'],
        dish_id=dish_id,
        quantity=quantity,
        total_cost=total_cost,
        delivery_address=delivery_address
    )

    # Save the order to the database
    db.session.add(order)
    db.session.commit()

    # Flash a success message
    flash('Your order has been placed.')

    # Redirect to the order confirmation page
    return redirect(url_for('order_confirmation'))

# Define the order confirmation page route
@app.route('/order_confirmation')
def order_confirmation():
    # Get the order ID
    order_id = request.args.get('order_id')

    # Find the order in the database
    order = Order.query.get(order_id)

    # Render the order confirmation page
    return render_template('order_confirmation.html', order=order)

# Define the login page route
@app.route('/login')
def login():
    return render_template('login.html')

# Define the login submission route
@app.route('/login', methods=['POST'])
def login_submit():
    # Get the username and password
    username = request.form.get('username')
    password = request.form.get('password')

    # Find the user in the database
    user = User.query.filter_by(username=username).first()

    # Check if the password is correct
    if user and check_password_hash(user.password_hash, password):
        # Create a session for the user
        session['user_id'] = user.id

        # Flash a success message
        flash('You have been logged in.')

        # Redirect to the home page
        return redirect(url_for('index'))

    # Flash an error message
    flash('Invalid username or password.')

    # Redirect back to the login page
    return redirect(url_for('login'))

# Define the signup page route
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Define the signup submission route
@app.route('/signup', methods=['POST'])
def signup_submit():
    # Get the username and password
    username = request.form.get('username')
    password = request.form.get('password')

    # Create a new user
    user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )

    # Save the user to the database
    db.session.add(user)
    db.session.commit()

    # Flash a success message
    flash('You have been signed up.')

    # Redirect to the login page
    return redirect(url_for('login'))

# Define the logout route
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()

    # Flash a success message
    flash('You have been logged out.')

    # Redirect to the home page
    return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

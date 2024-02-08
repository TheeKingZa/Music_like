#!/usr/bin/python3

from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages, jsonify
import json
from db import read_user_data, add_user_data

# Flask app instance
app = Flask(__name__)


# Load track data from songs.json
with open('data/songs.json', 'r') as file:
    tracks = json.load(file)

# Routes
@app.route('/')
def index():
    return render_template('login.html', current_page='/', tracks=tracks)

@app.route('/login', methods=['POST'])
def login():
    
    entered_username = request.form['username']
    entered_password = request.form['password']
    
    # Load user data
    user_data = read_user_data()
    
    # check if the entered user and paswd is matching
    for user in user_data:
        if user['username'] == entered_username and user['password'] == entered_password:
            return redirect(url_for('home'))
            # Redirect to home page if successful
    else:
        error = "Invalid Username or Password. Please Try Again"
        return render_template('login.html', current_page='login', error=error)

@app.route('/signup', methods=['POST'])
def signup():
    # Retrieve form data
    username = request.form.get('username')
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    # Validate form data (e.g., check for empty fields, validate email format, etc.)
    # Add your validation code here
    
    # Check if the passwords match
    if password != confirm_password:
        # Passwords don't match, handle this case (e.g., display an error message)
        error = "Passwords do not match."
        return render_template('sign-up.html', error=error, show_navbar=False)
    
    # Check if the user already exists (e.g., by querying the database)
    # Add your code to check if the user exists
    user_data = {
        'username': username,
        'name': name,
        'surname': surname,
        'email': email,
        'password': password
    }
    
    # If everything is valid, you can store the user in the database
    # Add your code to store the user in the database
    
    # For demonstration purposes, let's just redirect to the sign-up page again
    add_user_data(user_data)
    flash('Signup successful!', 'success')
    return redirect(url_for('home'))

@app.route('/signUp')
def signUp():
    # Render SignUp
    show_navbar = request.args.get('show_navbar', True)
    return render_template('sign-up.html', current_page='signUp', show_navbar=show_navbar)

@app.route('/home')
def home():
    # Render the home page
    messages = get_flashed_messages('success')
    return render_template('home.html', messages=messages, current_page='home')

@app.route('/search')
def search():
    search_query = request.args.get('query')
    # Simulate Database search
    search_results = [track for track in tracks if
                    search_query.lower() in track['title'].lower() or 
                    search_query.lower() in track['album'].lower() or
                    search_query.lower() in track['artist'].lower()]
    return jsonify(search_results)

@app.route('/contact')
def contact():
    # Render Contact page
    return render_template('contact.html', current_page='contact')

@app.route('/aboutus')
def aboutus():
    # Render AboutUs page
    return render_template('aboutus.html', current_page='aboutus')


    
if __name__ == '__main__':
    app.run(debug=True)

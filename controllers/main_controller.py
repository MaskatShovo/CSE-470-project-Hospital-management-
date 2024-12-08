from flask import Blueprint, render_template


main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('front.html')

@main_routes.route('/book-appointment')
def book_appointment():
    return render_template('question.html')

@main_routes.route('/show-availability')
def find_doctor():
    return render_template('doctor_avail.html')

@main_routes.route('/login')
def login():
    return render_template('login.html')

@main_routes.route('/create-account')
def signup():
    return render_template('signup.html')
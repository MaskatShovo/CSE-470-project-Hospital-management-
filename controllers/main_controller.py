# from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import create_user, get_user_by_email, update_user
from models.user_model import get_doctors_by_department
from models.user_model import add_health_record


main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('front.html')

@main_routes.route('/book-appointment')
def book_appointment():
    return render_template('question.html')

@main_routes.route('/emergency-contacts')
def emergency_contacts():
    return render_template('emer_contact.html')

@main_routes.route('/show-availability')
def find_doctor():
    return render_template('doctor_avail.html')

@main_routes.route('/login')
def login():
    return render_template('login.html')

@main_routes.route('/create-account')
def signup():
    return render_template('signup.html')

@main_routes.route('/question2-page')
def question2_page():
    return render_template('question2.html')

@main_routes.route('/doctors/<department>')
def doctors_by_department(department):
    doctors = get_doctors_by_department(department)
    return render_template('doctor_profiles.html', department=department.capitalize(), doctors=doctors)

# //////////////////////////////////////////////////////////////////////////

@main_routes.route("/create-account", methods=["GET", "POST"])
def signup1():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        nid = request.form["nid"]

        create_user(first_name, last_name, phone, email, password, nid)
        return redirect(url_for("main_routes.patient_profile", email=email))
    return render_template("signup.html")

@main_routes.route("/patient-profile/<email>")
def patient_profile(email):
    user = get_user_by_email(email)
    return render_template("patient_profile2.html", user=user)

@main_routes.route("/update-profile/<email>", methods=["GET", "POST"])
def update_profile(email):
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone = request.form["phone"]
        password = request.form["password"]
        nid = request.form["nid"]

        update_user(email, first_name, last_name, phone, password, nid)
        return redirect(url_for("main_routes.patient_profile", email=email))

    user = get_user_by_email(email)
    return render_template("update.html", user=user)

# ///////////////////////////////////////////
@main_routes.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]


        user = get_user_by_email(email)

      
        if user and user[5] == password:  
            return redirect(url_for("main_routes.patient_profile", email=email))
        else:

            return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")

@main_routes.route("/patient-profile/<email>")
def patient_profile3(email):
    user = get_user_by_email(email)
    if not user:
        return redirect(url_for("main_routes.login"))
    return render_template("patient_profile2.html", user=user)

@main_routes.route("/logout")
def logout():

    return redirect(url_for("main_routes.home"))

@main_routes.route('/health-record/<email>', methods=["GET", "POST"])
def health_record(email):
    user = get_user_by_email(email)
    if not user:
        return redirect(url_for('main_routes.login'))

    if request.method == "POST":
        weight = request.form["weight"]
        blood_pressure = request.form["blood_pressure"]
        heart_rate = request.form["heart_rate"]
        diabetes = 1 if request.form.get("diabetes") == "on" else 0
        high_pressure = 1 if request.form.get("high_pressure") == "on" else 0
        allergy = request.form["allergy"] or None

        add_health_record(user[0], weight, blood_pressure, heart_rate, diabetes, high_pressure, allergy)
        return redirect(url_for('main_routes.patient_profile', email=email))

    return render_template('health_record.html', user=user)


from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import create_user, get_user_by_email, update_user
from models.user_model import get_doctors_by_department
from models.user_model import add_health_record
from models.user_model import get_all_doctors_with_availability
from models.user_model import create_appointment, get_appointments_by_email, delete_appointment
from fpdf import FPDF
import io
from flask import send_file

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('front.html')

@main_routes.route('/book-appointment')
def book_appointment():
    return render_template('question.html')

@main_routes.route('/faq')
def faq():
    return render_template('faq.html')

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

@main_routes.route('/emergency_appointment-page/<email>')
def emergency_appointment(email):
    return render_template('emergency.html', email=email)


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


@main_routes.route("/doctor-availability")
def doctor_availability():
    doctors = get_all_doctors_with_availability()
    return render_template("doctor_avail.html", doctors=doctors)


# @main_routes.route('/dynamic', methods=['GET', 'POST'])
# def dynamic():
#     if request.method == 'POST':
#         email = request.form['email']  # Email of the logged-in user
#         date = request.form['date']
#         slot = request.form['slot']
#         doctor = request.form['doctor']
#         hospital = request.form['hospital']

#         create_appointment(email, date, slot, doctor, hospital)
#         return redirect(url_for('main_routes.patient_profile', email=email))

#     return render_template('dynamic.html')

@main_routes.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    if request.method == 'POST':
        email = request.form['email']
        date = request.form['date']
        slot = request.form['slot']
        doctor = request.form['doctor']
        hospital = request.form['hospital']

        create_appointment(email, date, slot, doctor, hospital)
        return redirect(url_for('main_routes.patient_profile', email=email))
    
 
    email = request.args.get('email')
    return render_template('dynamic.html', email=email)




@main_routes.route('/appointment-history/<email>', methods=['GET'])
def appointment_history(email):
    appointments = get_appointments_by_email(email)
    return render_template('appointment_history.html', appointments=appointments, email=email)

@main_routes.route('/cancel-appointment', methods=['POST'])
def cancel_appointment():
    appointment_id = request.form['appointment_id']
    email = request.form['email']
    delete_appointment(appointment_id)
    return redirect(url_for('main_routes.appointment_history', email=email))





@main_routes.route('/emergency', methods=['POST'])
def emergency():
    # Extract form data
    name = request.form.get('name')
    contact = request.form.get('contact')
    doctor = request.form.get('doctor')
    department = request.form.get('department')
    urgency = request.form.get('urgency')
    description = request.form.get('description')
    email = request.form.get('email')
    if not email:
        return "Email is missing in the form submission.", 400


    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)


    pdf.set_text_color(255, 0, 0)
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Indigo HealthCare", ln=True, align="C")


    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Contact: {contact}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.cell(200, 10, f"Doctor: {doctor}", ln=True)
    pdf.cell(200, 10, f"Department: {department}", ln=True)
    pdf.cell(200, 10, f"Urgency Level: {urgency}", ln=True)
    pdf.cell(200, 10, f"Description: {description}", ln=True)


    pdf_file = f"static/{name}_emergency_appointment.pdf"
    pdf.output(pdf_file)


    return {
        "file_url": url_for('static', filename=f"{name}_emergency_appointment.pdf"),
        "redirect_url": url_for('main_routes.patient_profile', email=email)
    }








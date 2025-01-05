# from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, redirect, url_for,flash
from models.user_model import create_user, get_user_by_email, update_user
from models.user_model import get_doctors_by_department
from models.user_model import add_health_record
from models.user_model import get_all_doctors_with_availability
from models.user_model import create_appointment, get_appointments_by_email, delete_appointment
from models.user_model import save_feedback
from models.user_model import save_cabin_booking
from models.user_model import save_test_booking
from models.user_model import get_feedback_data
from models.user_model import get_all_appointments_data
from models.user_model import get_cabin_bookings_by_email
from models.user_model import get_test_bookings_by_email
from models.user_model import get_all_users
from models.user_model import save_plan_booking
from models.user_model import get_plan_bookings_by_email

from models.user_model import (
    get_all_doctors,
    add_new_doctor,
    get_doctor_by_id,
    update_doctor,
    remove_doctor
)

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


@main_routes.route('/consultation-page')
def consultation():
    return render_template('consultation.html')

@main_routes.route('/hospital-features')
def hospital_features():
    return render_template('front_service.html')

@main_routes.route('/health-blogs')
def health_blogs():
    return render_template('health_blogs.html')


@main_routes.route('/login')
def login():
    return render_template('login.html')

@main_routes.route('/create-account')
def signup():
    return render_template('signup.html')

@main_routes.route('/question2-page')
def question2_page():
    return render_template('question2.html')

@main_routes.route('/question21-page')
def question21_page():
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
    
    # Get email from query parameters
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





class CustomPDF(FPDF):
    def header(self):

        self.set_fill_color(23, 110, 112)  
        self.set_text_color(255, 255, 255)  
        self.set_font("Arial", style="B", size=16)
        self.cell(0, 15, "Indigo HealthCare", ln=True, align="C", fill=True)
        self.ln(5) 

    def footer(self):
  
        self.set_y(-15)  
        self.set_fill_color(23, 110, 112)  
        self.set_text_color(255, 255, 255) 
        self.set_font("Arial", style="I", size=10)
        self.cell(0, 10, "Thank you for trusting Indigo HealthCare", align="C", fill=True)

@main_routes.route('/emergency', methods=['POST'])
def emergency():

    name = request.form.get('name')
    contact = request.form.get('contact')
    doctor = request.form.get('doctor')
    department = request.form.get('department')
    urgency = request.form.get('urgency')
    description = request.form.get('description')
    email = request.form.get('email')

    if not email:
        return "Email is missing in the form submission.", 400


    pdf = CustomPDF()
    pdf.add_page()


    pdf.set_text_color(0, 0, 0)  
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Contact: {contact}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.cell(200, 10, f"Doctor: {doctor}", ln=True)
    pdf.cell(200, 10, f"Department: {department}", ln=True)
    pdf.cell(200, 10, f"Urgency Level: {urgency}", ln=True)
    pdf.cell(200, 10, f"Description: {description}", ln=True)


    pdf.ln(20)


    pdf.set_fill_color(255, 0, 0)  
    pdf.set_text_color(255, 255, 255)  
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "THIS APPOINTMENT WILL BE PRIORITY", ln=True, align="C", fill=True)

    # Save PDF to static folder
    pdf_file = f"static/{name}_emergency_appointment.pdf"
    pdf.output(pdf_file)

    # Return the file URL to the frontend
    return {
        "file_url": url_for('static', filename=f"{name}_emergency_appointment.pdf"),
        "redirect_url": url_for('main_routes.patient_profile', email=email)
    }


@main_routes.route('/feedback-page/<email>')
def feedback_page(email):
    return render_template('feedback.html', email=email)

@main_routes.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        email = request.form['email'] 
        appointment_rating = request.form['appointment_rating']
        emergency_rating = request.form['emergency_rating']
        compatibility_rating = request.form['compatibility_rating']
        improvements = request.form['improvements']
        comments = request.form['comments']

        # Save feedback to the database
        save_feedback(email, appointment_rating, emergency_rating, compatibility_rating, improvements, comments)

        # Redirect back to patient profile page
        return redirect(url_for('main_routes.patient_profile', email=email))
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while saving feedback. Please try again.", 500

@main_routes.route('/service-listings/<email>')
def service_listings(email):
    return render_template('service_list.html', email=email)

@main_routes.route('/cabin-booking/<email>')
def cabin_booking(email):
    return render_template('cabin_booking.html', email=email)

@main_routes.route('/various-tests/<email>')
def various_tests(email):
    return render_template('various_tests.html', email=email)

@main_routes.route('/fitness-plan/<email>')
def fitness_plan(email):
    return render_template('fitness_plan.html', email=email)

@main_routes.route('/insurance-assistance/<email>')
def insurance_assistance(email):
    return render_template('insurance_assistance.html', email=email)

@main_routes.route('/book-cabin/<cabin_type>', methods=['POST'])
def book_cabin(cabin_type):
    try:
        email = request.form['email']
        booking_date = request.form['booking_date']

        # Save the booking to the database
        save_cabin_booking(email, cabin_type, booking_date)

        # Show a success message
        flash('Cabin booking successful!', 'success')
        return redirect(url_for('main_routes.patient_profile', email=email))
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while booking the cabin. Please try again.', 'error')
        return redirect(url_for('main_routes.service_listings', email=email))


@main_routes.route('/book-tests/<test_name>', methods=['POST'])
def book_tests(test_name):
    try:
        email = request.form['email']
        booking_date = request.form['booking_date']

        # Save booking data to the database
        save_test_booking(email, test_name, booking_date)

        # Show a success message
        flash('Test booking successful!', 'success')
        return redirect(url_for('main_routes.patient_profile', email=email))
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while booking the cabin. Please try again.', 'error')
        return redirect(url_for('main_routes.service_listings', email=email))
    
@main_routes.route('/book-plan/<plan_name>', methods=['POST'])
def book_fitness(plan_name):
    try:
        email = request.form['email']
        booking_date = request.form['booking_date']


        save_test_booking(email, plan_name, booking_date)


        flash('Test booking successful!', 'success')
        return redirect(url_for('main_routes.patient_profile', email=email))
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while booking the cabin. Please try again.', 'error')
        return redirect(url_for('main_routes.service_listings', email=email))







@main_routes.route('/appointments-subscriptions/<email>', methods=['GET'])
def appointments_subscriptions(email):
    try:
        # Fetch cabin bookings
        cabin_bookings = get_cabin_bookings_by_email(email)

        # Fetch test bookings
        test_bookings = get_test_bookings_by_email(email)

        return render_template(
            'appointments_subscriptions.html',
            email=email,
            cabin_bookings=cabin_bookings,
            test_bookings=test_bookings
        )
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while fetching your bookings. Please try again.", 500

#//////////////////////////////////////////////////////////////////////////////////////////////
@main_routes.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin.html')

@main_routes.route('/admin-login-page')
def admin_login_page():
    return render_template('admin_log.html')

@main_routes.route('/admin-login', methods=['POST'])
def admin_login():
    from models.user_model import validate_admin_password  # Import the function for validation

    password = request.form['password']

    # Validate the password using the database
    if validate_admin_password(password):
        return redirect(url_for('main_routes.admin_dashboard'))
    else:
        return render_template('admin_log.html', error="Invalid password!")



@main_routes.route('/feedback-analytics')
def feedback_analytics():
    from models.user_model import get_feedback_data

    # Fetch feedback data from the database
    feedback_data = get_feedback_data()

    # Pass data to the template
    return render_template('feedback_analytics.html', feedback_data=feedback_data)


@main_routes.route('/staff-management')
def staff_management():
    from models.user_model import get_all_doctors
    doctors = get_all_doctors()
    return render_template('staff_manage.html', doctors=doctors)

@main_routes.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        qualification = request.form['qualification']
        department = request.form['department']
        availability = request.form['availability']
        experience = request.form['experience']
        from models.user_model import add_new_doctor
        add_new_doctor(name, qualification, department, availability, experience)
        return redirect(url_for('main_routes.staff_management'))
    return render_template('add_doctor.html')

@main_routes.route('/edit-doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    from models.user_model import get_doctor_by_id, update_doctor
    if request.method == 'POST':
        name = request.form['name']
        qualification = request.form['qualification']
        department = request.form['department']
        availability = request.form['availability']
        experience = request.form['experience']
        update_doctor(id, name, qualification, department, availability, experience)
        return redirect(url_for('main_routes.staff_management'))
    doctor = get_doctor_by_id(id)
    return render_template('edit_doctor.html', doctor=doctor)

@main_routes.route('/delete-doctor/<int:id>', methods=['POST'])
def delete_doctor(id):
    from models.user_model import remove_doctor
    remove_doctor(id)
    return '', 204


@main_routes.route('/appointment-search')
def appointment_search():
    from models.user_model import get_all_appointments_data
    data = get_all_appointments_data()
    return render_template('appt_search.html', data=data)


@main_routes.route('/data-export')
def data_export():
    return render_template('data_export.html')


@main_routes.route('/export-patients')
def export_patients():
    from models.user_model import get_all_users  # Assuming you need a function to get all users
    import csv
    from flask import Response

    # Fetch all users
    users = get_all_users()

    # Create CSV in memory
    csv_data = "ID,First Name,Last Name,Phone,Email,NID\n"
    for user in users:
        csv_data += f"{user['id']},{user['first_name']},{user['last_name']},{user['phone']},{user['email']},{user['nid']}\n"

    # Return the file as a response
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=patients.csv"}
    )

@main_routes.route('/export-doctors')
def export_doctors():
    from models.user_model import get_all_doctors
    import csv
    from flask import Response

    # Fetch all doctors
    doctors = get_all_doctors()

    # Create CSV in memory
    csv_data = "ID,Name,Qualification,Department,Experience,Availability\n"
    for doc in doctors:
        csv_data += f"{doc['id']},{doc['name']},{doc['qualification']},{doc['department']},{doc['experience']},{doc['availability']}\n"

    # Return the file as a response
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=doctors.csv"}
    )


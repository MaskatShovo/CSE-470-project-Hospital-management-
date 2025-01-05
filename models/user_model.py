from flask_mysqldb import MySQL

mysql = None

def init_db(app):
    global mysql
    mysql = MySQL(app)



def create_user(first_name, last_name, phone, email, password, nid):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO users (first_name, last_name, phone, email, password, nid)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (first_name, last_name, phone, email, password, nid),
    )
    mysql.connection.commit()
    cursor.close()

def get_user_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def update_user(email, first_name, last_name, phone, password, nid):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        UPDATE users
        SET first_name = %s, last_name = %s, phone = %s, password = %s, nid = %s
        WHERE email = %s
        """,
        (first_name, last_name, phone, password, nid, email),
    )
    mysql.connection.commit()
    cursor.close()


def get_doctors_by_department(department):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT name, qualification, department_head, medical_college, experience
        FROM doctors
        WHERE department = %s
        """,
        (department,)
    )
    doctors = cursor.fetchall()
    cursor.close()
    return doctors

def add_health_record(user_id, weight, blood_pressure, heart_rate, diabetes, high_pressure, allergy):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO health_records 
        (user_id, weight, blood_pressure, heart_rate, diabetes, high_pressure, allergy)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, weight, blood_pressure, heart_rate, diabetes, high_pressure, allergy)
    )
    mysql.connection.commit()
    cursor.close()


def get_all_doctors_with_availability():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT name, qualification, availability 
        FROM doctors
    """)
    doctors = cursor.fetchall()
    cursor.close()
    return [{"name": doc[0], "qualification": doc[1], "availability": doc[2]} for doc in doctors]


def create_appointment(email, date, slot, doctor, hospital):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO appointments (email, date, slot, doctor, hospital)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (email, date, slot, doctor, hospital)
    )
    mysql.connection.commit()
    cursor.close()

def get_appointments_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM appointments WHERE email = %s", (email,))
    appointments = cursor.fetchall()
    cursor.close()
    return appointments

def delete_appointment(appointment_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    mysql.connection.commit()
    cursor.close()


def save_feedback(email, appointment_rating, emergency_rating, compatibility_rating, improvements, comments):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO feedback (email, appointment_rating, emergency_rating, compatibility_rating, improvements, comments)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (email, appointment_rating, emergency_rating, compatibility_rating, improvements, comments)
    )
    mysql.connection.commit()
    cursor.close()

def save_cabin_booking(email, cabin_type, booking_date):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO cabins_booking (email, cabin_type, booking_date)
        VALUES (%s, %s, %s)
        """,
        (email, cabin_type, booking_date)
    )
    mysql.connection.commit()
    cursor.close()

def save_test_booking(email, test_name, booking_date):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO tests_booking (email, test_name, booking_date)
        VALUES (%s, %s, %s)
        """,
        (email, test_name, booking_date)
    )
    mysql.connection.commit()
    cursor.close()

def save_plan_booking(email, plan_name, booking_date):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO fitness_plan_bookings (email, plan_name, booking_date)
        VALUES (%s, %s, %s)
        """,
        (email, plan_name, booking_date)
    )
    mysql.connection.commit()
    cursor.close()


def get_cabin_bookings_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT cabin_type, booking_date, created_at FROM cabins_booking WHERE email = %s", (email,))
    cabin_bookings = cursor.fetchall()
    cursor.close()
    return [{"cabin_type": booking[0], "booking_date": booking[1], "created_at": booking[2]} for booking in cabin_bookings]


def get_test_bookings_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT test_name, booking_date, created_at FROM tests_booking WHERE email = %s", (email,))
    test_bookings = cursor.fetchall()
    cursor.close()
    return [{"test_name": booking[0], "booking_date": booking[1], "created_at": booking[2]} for booking in test_bookings]

def get_plan_bookings_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT plan_name, booking_date, created_at FROM fitness_plan_bookings WHERE email = %s", (email,))
    plan_bookings = cursor.fetchall()
    cursor.close()
    return [{"plan_name": booking[0], "booking_date": booking[1], "created_at": booking[2]} for booking in plan_bookings]

# /////////////////////////////////////////////////////////////////////////////
def validate_admin_password(entered_password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password FROM admin")
    stored_password = cursor.fetchone()[0]
    cursor.close()


    return entered_password == stored_password


def get_feedback_data():
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            SUM(appointment_rating = 'good') AS appointment_good,
            SUM(appointment_rating = 'average') AS appointment_average,
            SUM(appointment_rating = 'poor') AS appointment_poor,
            SUM(emergency_rating = 'good') AS emergency_good,
            SUM(emergency_rating = 'average') AS emergency_average,
            SUM(emergency_rating = 'poor') AS emergency_poor,
            SUM(compatibility_rating = 'good') AS compatibility_good,
            SUM(compatibility_rating = 'average') AS compatibility_average,
            SUM(compatibility_rating = 'poor') AS compatibility_poor
        FROM feedback
    """)
    result = cursor.fetchone()
    cursor.close()


    return {
        "Appointment Good": result[0],
        "Appointment Average": result[1],
        "Appointment Poor": result[2],
        "Emergency Good": result[3],
        "Emergency Average": result[4],
        "Emergency Poor": result[5],
        "Compatibility Good": result[6],
        "Compatibility Average": result[7],
        "Compatibility Poor": result[8],
    }



#///////////////////////////////////////

def get_all_doctors():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    return [{"id": doc[0], "name": doc[1], "qualification": doc[2], "department": doc[3], "availability": doc[7], "experience": doc[6]} for doc in doctors]

def add_new_doctor(name, qualification, department, availability, experience, medical_college=None, department_head=None):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO doctors (name, qualification, department, availability, experience, medical_college, department_head)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, qualification, department, availability, experience, medical_college, department_head))
    mysql.connection.commit()
    cursor.close()


def get_doctor_by_id(doctor_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()
    cursor.close()
    return doctor

def update_doctor(doctor_id, name, qualification, department, availability, experience):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE doctors
        SET name = %s, qualification = %s, department = %s, availability = %s, experience = %s
        WHERE id = %s
    """, (name, qualification, department, availability, experience, doctor_id))
    mysql.connection.commit()
    cursor.close()

def remove_doctor(doctor_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
    mysql.connection.commit()
    cursor.close()


def get_all_appointments_data():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            a.email, a.date, a.slot, a.doctor, a.hospital, 
            c.cabin_type, c.booking_date AS cabin_booking_date, 
            t.test_name, t.booking_date AS test_booking_date
        FROM appointments a
        LEFT JOIN cabins_booking c ON a.email = c.email
        LEFT JOIN tests_booking t ON a.email = t.email
    """)
    results = cursor.fetchall()
    cursor.close()


    return [
        {
            "email": row[0],
            "date": row[1],
            "slot": row[2],
            "doctor": row[3],
            "hospital": row[4],
            "cabin_type": row[5],
            "cabin_booking_date": row[6],
            "test_name": row[7],
            "test_booking_date": row[8],
        }
        for row in results
    ]

def get_all_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, first_name, last_name, phone, email, nid FROM users")
    users = cursor.fetchall()
    cursor.close()
    return [{"id": user[0], "first_name": user[1], "last_name": user[2], "phone": user[3], "email": user[4], "nid": user[5]} for user in users]

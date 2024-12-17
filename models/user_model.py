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


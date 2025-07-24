#!/usr/bin/env python3
import utilities as util
import mysql.connector
from mysql.connector import Error

class Student:
    def __init__(self, Reg_No, name, email, password, utme_score, state_of_origin, ssce_score, grades):
        self.Reg_No = Reg_No
        self.name = name
        self.email = email
        self.password = password
        self.utme_score = utme_score
        self.state_of_origin = state_of_origin
        self.ssce_score = ssce_score
        self.grades = grades

# Database config
try: 
    connection = mysql.connector.connect(
        host='mysql-2008-alustudent-3086.f.aivencloud.com',
        port='15699',
        user='avnadmin',
        password='AVNS_1DzsuhCNrX8Dsvjg2wA',
        database='APPLY_NAIJA',
        ssl_disabled=False
    )
except mysql.connector.Error as e:
    print(f"Error: {e} ⚠ Connection Error!")
    connection = None

def email_exists(email, user_type):
    cursor = connection.cursor()
    if user_type == "student":
        query = "SELECT 1 FROM students WHERE email = %s"
    else:
        query = "SELECT 1 FROM officers WHERE email = %s"

    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    return bool(result)

def reg_no_exists(reg_no):
    cursor = connection.cursor()
    query = "SELECT 1 FROM students WHERE Reg_No = %s"
    cursor.execute(query, (reg_no,))
    result = cursor.fetchone()
    cursor.close()
    return bool(result)

def signup_student():
    if not connection or not connection.is_connected():
        print("❌ Cannot connect to the database.")
        return

    grade_holder = []
    util.clear_terminal()
    print("Create Applicant Account")

    name = input("Full name: ").strip()
    email = input("Email: ").strip()

    if email_exists(email, "student"):
        print("❌ Email already in use!")
        input("Press Enter to return...")
        return

    password = input("Password: ").strip()
    state = input("State of origin: ").strip()

    reg_no = input("Registration Number: ").strip() #Makes sure to add length checks.
    if reg_no_exists(reg_no):
        print("❌ Registration number already in use!")
        input("Press Enter to return...")
        return

    # SSCE subject count input
    while True:
        try:
            num_subjects = int(input("How many SSCE subjects did you write? "))
            if num_subjects < 7 or num_subjects > 9:
                print("❌ The required number of subjects is 7 - 9.")
                continue
            break
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
    
    # Grade entry
    print("\nEnter subject and grade (e.g., Mathematics, A1):")
    for i in range(1, num_subjects + 1):
        while True:
            entry = input(f"Subject {i}: ").strip()
            if ',' not in entry:
                print("❌ Format error, use 'Subject, Grade'")
                continue
            grade_holder.append(entry)
            break

    ssce_score = ""
    for entry in grade_holder:
        score = entry[-2:]
        ssce_score += score + " "

    # UTME score input
    while True:
        utme = input("\nEnter your JAMB UTME score: ").strip()
        try:
            utme_score = int(utme)
            if utme_score < 0 or utme_score > 400:
                print("❌ UTME score must be between 0 and 400.")
                continue
            break
        except ValueError:
            print("❌ Invalid input! Enter a number.")
            continue

    # Create student object
    student = Student(
        reg_no, name, email, password,
        utme_score, state, ssce_score.strip(), grade_holder
    )

    # Insert into database
    cursor = connection.cursor()
    query = """
        INSERT INTO students (Reg_No, name, email, password, utme_score, state_of_origin, ssce_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        student.Reg_No, student.name, student.email, student.password,
        student.utme_score, student.state_of_origin, student.ssce_score
    )
    try:
        cursor.execute(query, values)
        connection.commit()
        util.clear_terminal()
        print(f"\n✅ Registration successful!")
        print("Your SSCE subject grades will be available in your dashboard.")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    signup_student()
    if connection and connection.is_connected():
        connection.close()





    input("Press Enter to continue...")
    def signup_officer():
     clear_terminal()
    print("Create Admissions Officer Account")
    name = input("Full name: ").strip()
    email = input("Official email: ").strip()

    if email_exists(email, "officer"):
        print("❌ Email already registered!")
        input("Press Enter to continue...")
        #return

    password = input("Create password: ").strip()
    university_name = input("University name: ").strip()
    university_ID = input("university _code: ").strip()

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("⚠ Cannot connect to database to register officer.")
            input("Press Enter to continue...")
            #return
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO officers (name, email, password, university_name,university_code)
            VALUES (%s, %s, %s, %s,%s)
        """, (name, email, password, university_name, university_ID))
        conn.commit()
        print("✅ Admissions officer account created successfully!")
    except Error as e:
        print(f"⚠ Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    input("Press Enter to continue...")


def login_student():
    clear_terminal()
    print("Student Login")

    for attempt in range(2, 0, -1):
        email = input("Email: ").strip()
        password = input("Password: ").strip() 
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                print("⚠ Cannot connect to database to login.")
                input("Press Enter to continue...")
                return
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE email = %s AND password = %s", (email, password))
            student = cursor.fetchone()
            if student:
                print(f"\n✅ Login successful! Welcome {student['name']}!")
                input("Press Enter to continue...")
                return
            else:
                print(f"\n❌ Invalid credentials ({attempt-1} attempts left)")
        except Error as e:
            print(f"⚠ Database Error: {e}")
            break
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    print("\n🚫 Login failed.")
    input("Press Enter to continue...")

def login_officer():
    clear_terminal()
    print("Admissions Officer Login")

    for attempt in range(2, 0, -1):
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                print("⚠ Cannot connect to database to login.")
                input("Press Enter to continue...")
                return
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM officers WHERE email = %s AND password = %s", (email, password))
            officer = cursor.fetchone()
            if officer:
                print(f"\n✅ Login successful! Welcome {officer['name']}!")
                input("Press Enter to continue...")
                return
            else:
                print(f"\n❌ Invalid credentials ({attempt-1} attempts left)")
        except Error as e:
            print(f"⚠ Database Error: {e}")
            break
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    print("\n🚫 Login failed.")
    input("Press Enter to continue...")

def welcome():
    while True:
        util.clear_terminal()
        print("Welcome to a Centralized Tertiary Education Application System for Nigerian Universities\n")
        print("Do you want to:")
        print("1. Login")
        print("2. Signup")
        choice = input("Select (1 or 2)").strip()

        if choice == "1":
            util.clear_terminal()
            print("1. Student Login")
            print("2. Admissions Officer Login")
            sub = input("Choose: ").strip()
            if sub == "1":
                login_student()
            elif sub == "2":
                login_officer()
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

        elif choice == "2":
            util.clear_terminal()
            print("--- Account Type ---")
            print("1. Create applicant account")
            print("2. Create admissions officer account")
            sub = input("Choose: ").strip()
            if sub == "1":
                signup_student()
            elif sub == "2":
                signup_officer()
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

        else:
            print("❌ Invalid choice!")
            input("Press Enter to continue...")

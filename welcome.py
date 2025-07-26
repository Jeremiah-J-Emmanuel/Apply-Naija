#!/usr/bin/env python3
import utilities as util
import mysql.connector
from student_env import load_student_env
from officer_env import load_officer_env
import time

# Defining the Student and Officer classes
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


class Officer:
    def __init__(self, name, email, password, university, code):
        self.name = name
        self.email = email
        self.password = password
        self.university = university
        self.code = code


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


def unikey_match(key, university):
    cursor = connection.cursor()
    query = "SELECT id FROM universities WHERE name = %s or acronym = %s"
    cursor.execute(query, (university, university))
    code = cursor.fetchone()
    cursor.close()
    try:
        if code[0] == int(key):
            return True
        else:
            print("The code you have provided is not the code for the university that you have entered!")
            print("Try Again!")
            return False
    except ValueError:
        print("Provide a code of numbers")
        return False
    
def password_match(email, password, user_type):
    cursor = connection.cursor()
    if user_type == "student":
        query = "SELECT password FROM students WHERE email = %s"
    else:
        query = "SELECT password FROM officers WHERE email = %s"    
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    if result[0] == password:
        return True
    else:
        return False





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
        INSERT INTO students (Reg_No, name, email, password, utme_score, state_of_origin, ssce_score, grades)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        student.Reg_No, student.name, student.email, student.password,
        student.utme_score, student.state_of_origin, student.ssce_score, ' '.join(student.grades)
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

    util.clear_terminal()
    print("Redirecting to yor dashboard...")
    time.sleep(1.5)
    load_student_env(student)





def signup_officer():
    util.clear_terminal()
    print("Create Admissions Officer Account")
    while True:
        name = input("Full name: ").strip()
        if not name: #if user does not input name
            print("Enter your name!")
            continue
        else:
            break

    while True:
        email = input("Official email: ").strip()
        if not email:
            print("Enter an email")
            continue
        elif "@" not in email or ".com" not in email:
            print("Enter a valid Email")
            continue
        elif email_exists(email, "officer"):
            print("❌ Email already registered!")
            print("Enter an email that is not registered")
            continue
        else:
            break
    while True:
        password = input("Create password: ").strip()
        if not password:
            print("Enter a password!")
            continue
        else:
            break
    print("Enter the University ID given to your university by JAMB")
    while True:
        university_ID = input("university _code: ").strip()
        print("Enter the exact University name or acronym")
        print("Example: Pan-Atlantic University name or PAU")
        university_name = input("University or acronymn name: ").strip()
        if unikey_match(university_ID, university_name):
            break
        else:
            continue


    officer = Officer(name, email, password, university_name, university_ID)
    cursor = connection.cursor() 
    query = ("INSERT INTO officers (name, email, password, university, University_ID) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query, (officer.name, officer.email, officer.password, officer.university, officer.code))
    print(f"\n✅ Registration successful! Welcome {officer.name}!")
    connection.commit()
    cursor.close()

    util.clear_terminal()
    print("Redirecting to yor dashboard...")
    time.sleep(1.5)
    load_officer_env(officer)


def login_student():
    util.clear_terminal()
    print("Login to student portal")
    while True:
        email = input("Email: ").strip()
        if not email:
            print("Email cannot be empty!")
            continue
        elif not email_exists(email, "student"):
            print("❌ Email not registered!")
            print("Please signup first.")
            input("Press Enter to continue...")
            return
        else:
            break
    
    count = 0
    while True:
        if count > 3:
            print("You have three failed attemps. Two more failed attempts, you will be logged out!")
        password = input("Password: ").strip()
        if not password:
            print("\nPassword cannot be empty!")
            count += count + 1
            continue
        elif not password_match(email, password, "student"):
            print("\n❌ Incorrect password!")
            print("Please try again.")
            count += count + 1
            continue
        else:
            break

    cursor = connection.cursor()
    query = ("SELECT * FROM students WHERE email = %s")
    cursor.execute(query, (email,))
    row = cursor.fetchone()
    student = Student(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    cursor.close()

    print(f"\n✅ Login successful! Welcome {student.name}!")
    print("Loading your dashboard...")
    time.sleep(1.5)
    load_student_env(student)


def login_officer():
    util.clear_terminal()
    print("Admissions Officer Login")
    while True:
        email = input("Email: ").strip()
        if not email:
            print("Email cannot be empty!")
            continue
        elif not email_exists(email, "officer"):
            print("❌ Email not registered!")
            print("Please signup first.")
            input("Press Enter to continue...")
            return
        else:
            break
        
    while True:
        password = input("Password: ").strip()
        if not password:
            print("Password cannot be empty!")
            continue
        elif not password_match(email, password, "officer"):
            print("❌ Incorrect password!")
            print("Please try again.")
            continue
        else:
            break


    cursor = connection.cursor()
    query = "SELECT * FROM officers WHERE email = %s"
    cursor.execute(query, (email,))
    row = cursor.fetchone()
    officer = Officer(row[1], row[2], row[3], row[4], row[5])
    cursor.close()

    print(f"\n✅ Login successful! Welcome {officer.name}!")
    print("Loading your dashboard...")
    time.sleep(1.5)
    load_officer_env(officer)


def welcome():
    while True:
        util.clear_terminal()
        print("Welcome to a Apply Naija, The Centralized Tertiary Education Application System for Nigerian Universities\n")
        print("Do you want to:")
        print("1. Login")
        print("2. Signup")
        choice = input("Select [1 or 2] ").strip()

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
                print("\n❌ Invalid choice!")
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

if __name__ == "__main__":
    welcome()
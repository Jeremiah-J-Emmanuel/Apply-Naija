#!/usr/bin/env python3
import os # Toolbox for clearing and working with files
import json # Tooolbox for saving and loading user data

Users_File= "users.json" # File to store all user account information
University_Codes = {  # Dictionary of university codes and their names
    "1001": "University of Ibadan, Oyo State",
    "1002": "University of Lagos, Lagos State",
    "1003": "Federal University of Technology Owerri, Imo State",
    "1004": "Ahmadu Bello University, Kaduna State",
    "1005": "Polytechnic of Calabar, Cross River State",
    "1006": "University of Abuja, Abuja",
    "1007": "University of Jos, Plateau state",
    "1008": "Nile University, Abuja",
    "1009": "University of Maiduguri",
    "1010": "University of Nigeria Nsukka, Enugu State",
    "1012": "Pan-Atlantic University, Lagos State",
    "1013": "Covenant University, Ogun State",
    "1014": "Baze University, Abuja",
    "1015": "Babcock University, Ogun State",
    "1016": "Landmark University, Kwara State",
    "1017": "Afe Babalola University, Ekiti State",
    "1018": "University of Port Harcourt, Rivers State",
    "1019": "University of Benin, Edo State",
    "1020": "Nigerian British University, Abia State"
}
#settings for connecting to the university database
Config= {
    'host': 'mysql-2008-alustudent-3086.f.aivencloud.com',
    'port': '15699',
    'user': 'avnadmin',
    'password': 'AVNS_1DzsuhCNrX8Dsvjg2wA',
    'database': 'APPLY_NAIJA',
    'ssl_disabled': False
}

def clear_terminal():          # Function to clear the terminal screen

    os.system('cls' if os.name == 'nt' else 'clear')   # clear the terminal based an Os
def load_users():            # function to load users from the JSON file
    if not os.path.exists(Users_File):    # check if the file exists
        return []   # if not, return an empty list
    with open(Users_File, 'r') as f:   # open the file in read mode  
        return json.load(f)      # convert JSON data to python dictionary

def save_users(users):   #functiont o save users to the JSON file
    with open(Users_File, 'w') as f:
        json.dump(users, f, indent=4)   # indent =4 spaces for better reading

def email_exists(email):    # function to check if an email already exists
    users = load_users()    # load users from the file
    return any(user['email'] == email for user in users)   #returns true if any user matches the email

def get_db_connection():    # function to connect to the university database
    try:    # trying to conect using config settings
        connection = mysql.connector.connect(**Config)
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")  # if connection fails,the message is displayed
        return None 

def verify_university_code(code):    # function to check if university code is valid
    if code in University_Codes:     
        return University_Codes[code]   # return university name if found
    
    # if not found locally, chech the main database
    connection = get_db_connection()
    if connection:      # If connection succeeded
        try:
            cursor = connection.cursor()  # Create a cursor
            cursor.execute("SELECT name FROM universities WHERE code = %s", (code,))
            result = cursor.fetchone()
            if result:   # If we got a result
                return result[0]   # Return a university name
        except mysql.connector.Error as e:
            print(f"Database query error: {e}")
        finally:
            connection.close() # Always close the connection once done to be used
    return None

            #------------- Entry point --------------

def welcome():      # welcome menu that navigates to login/signup 
    clear_terminal()
    print("Welcome to Centralized Tertiary Education Application System for Nigerian Universities\n")
    print("1. Login")
    print("2. Create your Account")
    choice = input("Select 1 or 2: ")

    if choice == "1":
        clear_terminal()
        print("1. Admissions Officer")
        print("2. Applicant")
        sub = input("Select 1 or 2: ")
        if sub == "1":
            login_university()
        elif sub == "2":
            login_student()
        else:
            print("❌ Invalid selection.")
            input("Press Enter to return to main menu...")
            welcome()
    elif choice == "2":
        clear_terminal()
        print("1. Admissions Officer Account")
        print("2. Applicant Account")
        sub = input("Select 1 or 2: ")
        if sub == "1":
            signup_university()
        elif sub == "2":
            signup_student()
        else:
            print("❌ Invalid selection.")
            input("Press Enter to return to main menu...")
            welcome()
    else:
        print("❌ Invalid input.")
        input("Press Enter to return to main menu...")
        welcome()


            #--------SIGNUP PART--------

def signup_student():    # handles signup for new students
    clear_terminal()     # Clear the screen
    print("Create a New Applicant Account")  # Prompt message 
    name = input("Full name: ")   # Get user's name
    email = input("Email: ")  # Get user's email

    if email_exists(email):    #checking if email already in use
        print("Email already in use.")
        input("Press Enter to return to main menu...")
        welcome()
        return

    password = input("Password: ")
    users = load_users()
    users.append({       # Add new student user to the list
        "email": email,
        "password": password,
        "name": name,
        "type": "student"
    })
    save_users(users)     # Save the updated user list 
    print("✅ Student account created successfully.")
    input("Press Enter to return to login...")
    welcome()     # Go  back to main menu

def signup_university():     # Handles signup for admission officers
    clear_terminal()
    print("Create a New Admissions Officer Account")
    name = input("University Name: ")
    email = input("Email: ")

    if email_exists(email):  # Preventing duplicated emails
        print("Email already in use.")
        input("Press Enter to return to main menu...")
        welcome()
        return

    code = input("Enter university code to verify: ")
    university_name = verify_university_code(code)  #check if university code is valid
    if not university_name:    # If not found, error message is displayed
        print("❌ Invalid university code. please try again.")
        input("Press Enter to return to main menu...")
        welcome()
        return
    password = input("Password: ")   #setting passwordd
    users = load_users()
    users.append({     #Add new officer with university information
        "Email": email,
        "Password": password,
        "Name": name,
        "Type": "officer",
        "University_code": code,
        "Verified_university": university_name
    })
    save_users(users)
    print(f"✅ Admissions officer account created for {university_name}.")
    input("Press Enter to return to login...")
    welcome()

            #---------- LOGIN PART -------------

def login_student():     # Function to handle login for students
    clear_terminal()
    attempts_left = 3
    
    print("Applicant Login\n")
    
    while attempts_left > 0:
        email = input("Email: ")
        password = input("Password: ")
        
        users = load_users()   # load all users
        user_found = False
        
        # First check if email exists
        for user in users:
            if user['email'] == email:
                user_found = True
                if user['password'] == password and user['type'] == 'student':
                    print("\n✅ Login successful!!")
                    print(f"Welcome, {user['name']} (Student)")
                    return user
                break
        
        attempts_left -= 1
        
        if not user_found:
            print("\n Email not found in our system")
        else:
            print("\n❌ Incorrect password")
            
        if attempts_left > 0:
            print(f"Please try again ({attempts_left} {'attempt' if attempts_left == 1 else 'attempts'} remaining)\n")
        else:
            print("\n Maximum attempts reached")
            return None

def login_university():   # Function to handle login for the admission officers
    clear_terminal()
    attempts_left = 3
    
    print("Admissions Officer Login\n")
    
    while attempts_left > 0:
        email = input("Email: ")
        password = input("Password: ")
        
        users = load_users()
        user_found = False
        
        # First check if email exists
        for user in users:
            if user['email'] == email:
                user_found = True
                if user['password'] == password and user['type'] == 'officer':
                    print("\n✅ Login successful!")
                    print(f"Welcome to {user['name']} as (Officer)")
                    print(f"University: {user.get('verified_university', 'Not specified')}")
                    return user
                break
        
        attempts_left -= 1
        
        if not user_found:
            print("\n Email not found in our system")
        else:
            print("\n❌ Incorrect password")
            
        if attempts_left > 0:
            print(f"Please try again ... ({attempts_left} {'attempt' if attempts_left == 1 else 'attempts'} remaining)\n")
        else:
            print("\n🚫 Maximum attempts reached")
            return None


if _name_ == "_main_":
    welcome()

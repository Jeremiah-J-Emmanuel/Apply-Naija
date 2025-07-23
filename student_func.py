<<<<<<< HEAD
def send_application(name): print(f"Sending application for {name}..."); input("Press Enter to continue.")

def withdraw_application(name): print(f"Withdrawing application for {name}..."); input("Press Enter to continue.")

def edit_general_info(name): print(f"Editing info for {name}..."); input("Press Enter to continue.")

def search_universities(): print("Searching universities..."); input("Press Enter to continue.")

def check_application_status(name): print(f"Checking application status for {name}..."); input("Press Enter to continue.")

def home_bar(name): print(f"This is {name}'s home bar..."); input("Press Enter to continue.")
=======
#!/usr/bin/env python3
import utilities as util
import mysql.connector

try: 
    connection = mysql.connector.connect(
    host = 'mysql-2008-alustudent-3086.f.aivencloud.com',
    port = '15699',
    user = 'avnadmin',
    password = 'AVNS_1DzsuhCNrX8Dsvjg2wA',
    database = 'APPLY_NAIJA',
    ssl_disabled = False)
    cursor = connection.cursor()

except mysql.connector.Error as e:
    print(f"Error: {e}")

def send_app():
    util.clear_terminal()
    print('"Education is the most powerful weapon which you can use to change the world." -Nelson Mandela')
    print(" Send in your univesity application, and get ready to change the world!")
    print("----------------------------------------------------------------------------------------------")

    while True:
        university = input("Enter the name of the University: ")
        query = "SELECT * FROM universities WHERE name = %s"
        cursor.execute(query, (university,))

        # Fetch one matching record (if any)
        result = cursor.fetchone()
        if result:
            break
        else:
            print("University not found. Try Again.")
            continue
        
    cursor.close()
    connection.close()

def send_or_withdraw():
    util.clear_terminal()
    print("SEND OR WITHDRAW AN APPLICATION FROM A UNIVERSITY")
    print("-------------------------------------------------")
    print("Do you want to send or withdraw an application(S or W)")
    while True:
        ans = input("Choose S or W").strip().lower()
        if not ans: #if the user does not enter a value
            print("Please enter an option")
            continue
        elif ans != "s" or ans != "w":
            print("")
        elif ans == "s":
            util.clear_terminal()
            send_app()
        else:
            util.clear_terminal()
            withdraw_app()

send_app()


import os

# Example scholarship database (replace with your actual data source)
scholarships_db = [
    {"name": "MTN Foundation Scholarship", "amount": "N200,000", "university": "University of Lagos"},
    {"name": "NNPC/Total Scholarship", "amount": "N150,000", "university": "University of Ibadan"},
    {"name": "Agbami Medical Scholarship", "amount": "N100,000", "university": "Ahmadu Bello University"},
]

# Example university database (replace with your actual data source)
university_db = [
    {"name": "University of Lagos", "state": "Lagos State"},
    {"name": "University of Ibadan", "state": "Oyo State"},
    {"name": "Federal University of Technology Owerri", "state": "Imo State"},
    {"name": "Ahmadu Bello University", "state": "Kaduna State"},
    {"name": "Polytechnic of Calabar", "state": "Cross River State"},
    {"name": "University of Abuja", "state": "Abuja"},
    {"name": "University of Jos", "state": "Plateau State"},
    {"name": "Nile University", "state": "Abuja"},
    {"name": "Obafemi Awolowo University", "state": "Oyo State"},
    {"name": "University of Maiduguri", "state": "Borno State"},
    {"name": "University of Nigeria Nsukka", "state": "Enugu State"},
    {"name": "Pan-Atlantic University", "state": "Lagos State"},
    {"name": "Covenant University", "state": "Ogun State"},
    {"name": "Baze University", "state": "Abuja"},
    {"name": "Babcock University", "state": "Ogun State"},
    {"name": "Landmark University", "state": "Kwara State"},
    {"name": "Afe Babalola University", "state": "Ekiti State"},
    {"name": "University of Port Harcourt", "state": "Rivers State"},
    {"name": "University of Benin", "state": "Edo State"},
    {"name": "Nigerian British University", "state": "Abia State"},
]

def scholarship_list():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Available Scholarships:\n")
    if not scholarships_db:
        print("No scholarships available at the moment.")
    else:
        for idx, scholarship in enumerate(scholarships_db, 1):
            print(f"{idx}. {scholarship['name']} - {scholarship['amount']} ({scholarship['university']})")
    input("\nPress Enter to return to menu...")

def search_bar():
    os.system('cls' if os.name == 'nt' else 'clear')
    criterion = input("Enter university name or state: ").strip().lower()
    results = [
        uni for uni in university_db
        if criterion in uni['name'].lower() or criterion in uni['state'].lower()
    ]
    print()
    if results:
        print("Search Results:")
        for idx, uni in enumerate(results, 1):
            print(f"{idx}. {uni['name']} - {uni['state']}")
    else:
        print("No schools found.")
    input("\nPress Enter to return to menu...")
>>>>>>> e82332fbcb7f4ea57a15b8d4a4477ec875a736dd

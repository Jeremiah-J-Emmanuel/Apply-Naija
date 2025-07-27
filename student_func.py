#!/usr/bin/env python3

import utilities as util
import mysql.connector
import time

try: 
    connection = mysql.connector.connect(
    host = 'mysql-2008-alustudent-3086.f.aivencloud.com',
    port = '15699',
    user = 'avnadmin',
    password = 'AVNS_1DzsuhCNrX8Dsvjg2wA',
    database = 'APPLY_NAIJA',
    ssl_disabled = False)

except mysql.connector.Error as e:
    print(f"Error: {e}", "Connect to the internet and Run the app again")



def send_app(student): #The fucntion for sending applications
    util.clear_terminal()
    print(" Send in your university 🏫 application, and get ready to change the world!")
    print("=" * 75)
    cursor = connection.cursor()

    print("Enter the exact name of the institution you want to apply to.")
    print("Example: University of Nigeria Nsukka")
    print("=" * 75)
    while True:
        university = input("\nEnter the exact name of the institution: ")
        query = "SELECT * FROM universities WHERE name = %s"
        cursor.execute(query, (university,))

        # Fetch one matching record (if any)
        result = cursor.fetchone()
        if result:
            print(f"Submitting application to {result[1]}")
            break
        else:
            print("School not found. Try Again.")
            continue

    while True:
        course = input("\nWhat is the course you want to study: ")
        if not course:
            print("Please enter a value")
            continue
        else:
            print("course successfully entered.")
            break
    print("=" * 100)
    print("Are You ready to submit you appliation")
    print("By clicking yes, you are consenting to your personal details being shared with the university")
    print("=" * 100)
    print("1. YES")
    print("2. NO")

    while True:
        ans = input("\nSubmit your application [Y/N]: ").lower().strip()
        if not ans:
            print("Enter a value:")
            continue
        elif ans != "y" and ans != "n":
            print("choose Y or N")
            continue
        elif ans == "y":
            app_table = result[3] + "_applicants"
            try: 
                # Creating the uni applicant table if it does not exist
                create_query = f"""
                CREATE TABLE IF NOT EXISTS {app_table}(
                    Reg_No VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(200),
                    email VARCHAR(255),
                    course VARCHAR(200),
                    SSCE_RESULT VARCHAR(20),
                    UTME_SCORE INT,
                    state_of_origin VARCHAR(30),
                    grades VARCHAR (500),
                    status VARCHAR(50)
                )
                """
                cursor.execute(create_query)
                #Submission
                query = f"INSERT INTO {app_table} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (student.Reg_No, student.name, student.email, course,
                                    student.ssce_score, student.utme_score, student.state_of_origin, ','.join(student.grades), 'Pending'))
                print("Application submitted successfully! 🎉")
                connection.commit()
                break                

            except mysql.connector.IntegrityError: #If the user has already submitted
                print("You have already Submitted an application!")
                print("You can go and check your application status")
                break

        else: #if ans == n
            print("Cancelling submission...")
            time.sleep(1.5)
            print("Submission cancelled!")
            break
    cursor.close()


def withdraw_app(student):
    util.clear_terminal()
    print("WITHDRAW AN APPLICATION FROM A UNIVERSITY")
    print("-------------------------------------------------")
    cursor = connection.cursor()

    while True:
        print("Enter the exact name of the institution you want to withdraw from.")
        print("Example: University of Ibadan")
        print("=" * 50)
        university = input("Enter the exact name of the institution: ")
        query = "SELECT * FROM universities WHERE  name = %s"
        cursor.execute(query, (university,))

        # Fetch one matching record (if any)
        result = cursor.fetchone()
        if result:
            print(f"Withdrawing application from {result[1]}")
            break
        else:
            print("University not found. Try Again.\n")
            continue

    while True:
        ans = input("Are you sure you want to withdraw your application? [Y/N]: ").lower().strip()
        if not ans:
            print("Please enter a value:")
            continue
        elif ans != "y" and ans != "n":
            print("Choose Y or N")
            continue
        elif ans == "y":
            util.clear_terminal()
            app_table = result[3] + "_applicants"
            create_query = f"""
            CREATE TABLE IF NOT EXISTS {app_table}(
                Reg_No VARCHAR(20) PRIMARY KEY,
                name VARCHAR(200),
                email VARCHAR(255),
                course VARCHAR(200),
                SSCE_RESULT VARCHAR(20),
                UTME_SCORE INT,
                state_of_origin VARCHAR(30),
                grades VARCHAR (500),
                status VARCHAR(50)
            )
            """
            cursor.execute(create_query)
            query = f"SELECT * FROM {app_table} WHERE Reg_No = {student.Reg_No}"
            cursor.execute(query)
            app_data = cursor.fetchone()

            if app_data:
                print(f"Withdrawing application from {result[1]}...")
                time.sleep(1.5)
                query = f"DELETE FROM {app_table} WHERE Reg_No = %s"
                cursor.execute(query, (student.Reg_No,))
                connection.commit
                print("Application withdrawn successfully! 🎉")
                break
            else:
                print("You have not submitted any application to this institution")
                break

        else: #if ans == n
            print("Cancelling withdrawal...")
            time.sleep(1.5)
            break

    cursor.close()


def send_or_withdraw(student): #You need to put a check incase the timeline has passed for sending applications
    util.clear_terminal()
    print("SEND OR WITHDRAW AN APPLICATION FROM A UNIVERSITY")
    print("-------------------------------------------------")
    print("Do you want to send or withdraw an application(S or W)")
    while True:
        ans = input("Choose S or W: ").strip().lower()
        if not ans: #if the user does not enter a value
            print("Please enter an option!")
            continue
        elif ans != "s" and ans != "w":
            print("Invalid Choice. Try agiain!")
            continue
        elif ans == "s":
            send_app(student)
            break
        else:
            withdraw_app(student)
            break
    input("\nPress Enter to return to the menu...")


def home_bar(student):
    util.clear_terminal()
    print("HOME BAR")
    print("=" * 75)
    print(f"Welcome to your Home Bar, {student.name}!")
    print("=" * 75)
    print("Here are your details:")
    print("=" * 75)
    print(f"Name: {student.name}")
    print(f"Email: {student.email}")
    print(f"Registration Number: {student.Reg_No}")
    print(f"UTME Score: {student.utme_score}")
    print(f"State of Origin: {student.state_of_origin}")
    print(f"SSCE Score: {student.ssce_score}")
    print(f"SSCE Grades: {(student.grades)}")

    input("\nPress Enter to return to the menu...")


def scholarship_list():
    util.clear_terminal()
    print("______________________________________________________________________________________")
    print('                               Available Scholarships')
    print("--------------------------------------------------------------------------------------")
    # scholarship database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM scholarships")
    rows = cursor.fetchall()
    for column in rows:
        print(f"{column[1]} | University: {column[2]} | Funding: {column[3]}")
        print("--------------------------------------------------------------------------------------")
    input("\nPress Enter to return to the menu...")
    cursor.close()


def search_bar():
    util.clear_terminal()
    print("WELCOME TO THE SEARCH BAR!")
    print("Search by Name or by State\n")

    criterion = input("Enter university name or state: ").strip()
    criterion = f"%{criterion}%"  # wildcards for LIKE

    query = "SELECT * FROM universities WHERE name LIKE %s OR state LIKE %s"
    cursor = connection.cursor()
    cursor.execute(query, (criterion, criterion))
    results = cursor.fetchall()

    if results:
        print("Search Results:")
        for row in results:
            print(f"{row[1]} - {row[2]}")
    else:
        print("No schools found.")

    input("\nPress Enter to return to menu...")


def edit_general_info(student): #This parameter is the student object
    util.clear_terminal()
    print("What would you like to update?")
    print("Note that these updates will not reflect in the applications that you have already submitted")
    print("=" * 75)
    print("1.Name")
    print("2.Email")
    print("3.Password")
    print("4.SSCE_score")
    print("=" * 75)
    choice = input("Enter your choice :")

    if choice == "1":
        cursor = connection.cursor()
        util.clear_terminal()
        while True:
            new_name = input("Enter your new name: ")
            if new_name:
                student.name = new_name
                update_query = "UPDATE students SET name = %s  WHERE Reg_No = %s"
                cursor.execute(update_query, (student.name, student.Reg_No))
                cursor.close()
                connection.commit()
                print(f"Name updated successfully to {student.name} !")
                enter = input("Press Enter to Continue ")
                break
            else:
                print("Enter a valid name!")
                continue

    elif choice == "2":
        util.clear_terminal()
        while True:
            cursor = connection.cursor()
            new_email = input("Enter your new email: ")
            if "@" not in new_email or "." not in new_email:
                print("Please enter a valid email address.")
                continue
            else:
                print("The next time you log in, use this email")
                student.email = new_email
                update_query = "UPDATE students SET email = %s WHERE Reg_No = %s"
                cursor.execute(update_query, (student.email, student.Reg_No))
                cursor.close()
                connection.commit()
                print(f"Email updated successfully to {student.email}")
                enter = input("Press Enter to Continue ")
                break

    elif choice == "3":
        util.clear_terminal()
        while True:
            cursor = connection.cursor()
            new_password = input("Enter your new password: ")
            if new_password:
                print("The next time you log in, use this password")
                student.password = new_password
                update_query = "UPDATE students SET password = %s WHERE Reg_No = %s"
                cursor.execute(update_query, (student.password, student.Reg_No))
                connection.commit()
                print("Password updated successfully")
                enter = input("Press Enter to Continue ")
                break
            else:
                print("Please input a password")
                continue

    elif choice == "4":
        grade_holder = []
        cursor = connection.cursor()
        util.clear_terminal()
        while True:
            try:
                num_subjects = int(input("How many SSCE subjects are you entering? "))
                if num_subjects < 7 or num_subjects > 9:
                    print("❌ The required number of subjects is 7 - 9.")
                    continue
                else:
                    break      
            except ValueError:
                print("❌ Invalid input! Please enter a number.")
                continue
        print("\nEnter subject and grade (e.g., Mathematics, A1):")
        for i in range(1, num_subjects + 1):
            while True:
                entry = input(f"Subject {i}: ").strip()
                if ',' not in entry:
                    print("❌ Format error, use 'Subject, Grade'")
                    continue
                else:
                    grade_holder.append[entry]
                    break

        ssce_score = ""
        for entry in grade_holder:
            score = entry[-2:]
            ssce_score += score + " "

        student.ssce_score = ssce_score
        student.grades = grade_holder

        update_query = "UPDATE students SET ssce_score = %s, grades = %s WHERE Reg_No = %s"
        cursor.execute(update_query, (student.ssce_score, ' '.join(student.grades), student.Reg))
        connection.commit()
        enter = input("Press Enter to Continue ")

    else:
        print("Invalid choice.")
        time.sleep(1)
        return


def check_application_statuses(user_id, conn):
    cursor = conn.cursor()
    query = "SELECT university_name, application_status FROM applications WHERE user_id=%s"
    try:
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        if results:
            print(f"\nApplication statuses for user ID {user_id}:")
            for university, status in results:
                print(f"- {university}: {status}")
        else:
            print("No applications found for this user.")
    except mysql.connector.Error as err:
        print("Database error:", err)



if __name__ == "__main__":
    search_bar()
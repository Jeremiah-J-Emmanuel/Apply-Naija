#!/usr/bin/env python3
from ast import While
import utilities as util
import mysql.connector
import time
from welcome import Student, Officer

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



def send_app(): #The fucntion for sending applications
    util.clear_terminal()
    print('"Education 🏫 is the most powerful weapon which you can use to change the world."-Nelson Mandela')
    print(" Send in your univesity application, and get ready to change the world!")
    print("=" * 50)
    cursor = connection.cursor()

    while True:
        print("Enter the exact name of the institution you want to apply to.")
        print("Example: University of Nigeria Nsukka")
        print("=" * 50)
        university = input("Enter the exact name of the institution: ")
        query = "SELECT * FROM universities WHERE name = %s"
        cursor.execute(query, (university,))

        # Fetch one matching record (if any)
        result = cursor.fetchone()
        if result:
            print(f"Submitting application to {result}")
            break
        else:
            print("University not found. Try Again.")
            continue

    while True:
        course = input("What is the course you want to study: ")
        if not course:
            print("Please enter a value")
            continue
        else:
            print("course successfully entered.")
            break
        
    print("Are You ready to submit you appliation")
    print("By clicking yes, you are consenting to your personal details being shared with the university")
    print("=" * 50)
    print("1. YES")
    print("2. NO")
    while True:
        ans = input("Submit your application [Y/N]: ").lower().strip()
        if not ans:
            print("Enter a value:")
            continue
        elif ans != "y" or ans != "n":
            print("choose Y or N")
            continue
        elif ans == "y":
            query = " "
            print("Application submitted successfully! 🎉")
        else: #if ans == n
            print("Cancelling submission")
            time.sleep(1.5)
            break

    cursor.close()
    print("Application submitted successfully! 🎉")


def withdraw_app():
    util.clear_terminal()
    print("WITHDRAW AN APPLICATION FROM A UNIVERSITY")
    print("-------------------------------------------------")
    cursor = connection.cursor()

    while True:
        print("Enter the exact name of the institution you want to withdraw from.")
        print("Example: University of Ibadan")
        print("=" * 50)
        university = input("Enter the exact name of the institution: ")
        query = "SELECT * FROM universities WHERE name = %s"
        cursor.execute(query, (university,))

        # Fetch one matching record (if any)
        result = cursor.fetchone()
        if result:
            print(f"Withdrawing application from {result}")
            break
        else:
            print("University not found. Try Again.")
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
            query = " "
            print("Application withdrawn successfully! 🎉")
            break
        else: #if ans == n
            print("Cancelling withdrawal")
            time.sleep(1.5)
            break

    cursor.close()



def send_or_withdraw(): #You need to put a check incase the timeline has passed for sending applications
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
            util.clear_terminal()
            send_app()
            break
        else:
            util.clear_terminal()
            withdraw_app()


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
    cursor.close()

def search_bar():
    util.clear_terminal()
    print("WELCOME TO THE SEARCH BAR!")
    print("Search by Name or by State\n")

    criterion = input("Enter university name or state: ").strip()
    criterion = f"%{criterion}%"  # Add wildcards for LIKE

    query = "SELECT * FROM universities WHERE name LIKE %s OR state LIKE %s"
    cursor.execute(query, (criterion, criterion))
    results = cursor.fetchall()

    if results:
        print("Search Results:")
        for row in results:
            print(f"{row[1]} - {row[2]}")
    else:
        print("No schools found.")

    input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    search_bar()



    def edit_general_info(student: Student): #This parameter is the student object
        util.clear_terminal
        print("What would you like to update?")
        print("1.Name")
        print("2.Email")
        print("3. Password")
        print("4. SSCE_score")

        choice =input("Enter your choice :")
        if choice == "1":
            cursor = connection.cursor()
            while True:
                new_name = input("Enter your new name: ")
                if new_name and new_name.isalpha():
                    student.name =new_name
                    update_query="UPDATE students SET name = %s  WHERE id = %s"
                    cursor.execute(update_query, (student.name, student.id))
                    cursor.close()
                    connection.commit()
                    print("Name updated successfully!")
                    break
                else:
                    print("Enter a valid name!")
                    continue

        elif choice == "2":
            cursor = connection.cursor()
            new_email= input ("Enter your new email:")
            print("The next time you log in, use this email")
            student.email = new_email
            update_query="UPDATE students SET email = %s WHERE id = %s"
            cursor.execute(update_query, (student.email, student.id))
            cursor.close()
            connection.commit()
            print("Email updated successfully!")

        elif choice =="3":
            new_phone =input("Enter your new phone number:")
            util.phone= new_phone
            update_query="UPDATE users SET phone=? WHERE id=?"
            data =(new_phone,util.id)
        else:
            print("Invalid choice.")
            return
        cursor =conn.cursor()
        cursor.execute(update_query,data)
        conn.commit()
        print ("Information updated successfully!")

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
#Admin function for Apply-Naija

import mysql.connector
import utilities as util
import time

def get_connection():
    return mysql.connector.connect(
        host='mysql-2008-alustudent-3086.f.aivencloud.com',
        port='15699',
        user='avnadmin',
        password='AVNS_1DzsuhCNrX8Dsvjg2wA',
        database='APPLY_NAIJA',
        ssl_disabled=False
    )

def review_app(officer):
    util.clear_terminal()
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get the university ID
        cursor.execute("SELECT * FROM universities WHERE name = %s", (officer.university,))
        result = cursor.fetchone()

        if not result:
            print(f" No university found with name {officer.university}")
            input("\nPress Enter to return to the dashboard.")
            return

        acronym = result['acronym'] #This is because it returns a dictionary
        applicant_table = acronym + "_applicants"

        # Fetch only pending student applications
        query = f"SELECT * FROM {applicant_table} WHERE status <> 'Admitted' AND status <> 'Rejected'" 
        cursor.execute(query)
        applications = cursor.fetchall()

        if not applications:
            print(f" No applications yet to {officer.university}")
            input("\nPress Enter to return to the dashboard.")
            return
        else:
            util.clear_terminal()
            print(f"\n Applications for {officer.university}")
            for app in applications:
                print("=" * 75)
                print(f"Name: {app['name']}")
                print(f"Student Reg_No: {app['Reg_No']}")
                print(f"Student Email: {app['email']}")
                print(f"Intended Course: {app['course']}")
                print(f"JAMB UTME: {app['UTME_SCORE']}")
                print(f"SSCE Grades: {app['grades']}")
                print(f"State of Origin: {app['state_of_origin']}")
                print(f"SSCE result Summary: {app['SSCE_RESULT']}")
                print("=" * 75)

                print("Make a decision on this application")
                while True:
                    decision = input("Admit or Deny or Waitlist [A/D/W]: ").lower().strip()
                    if not decision:
                        print("Enter a value \n")
                        continue
                    elif decision != "a" and (decision != "d" and decision != "w"):
                        print("Please Enter the right Value\n")
                        continue
                    elif decision == "a":
                        query = f"UPDATE {applicant_table} SET status = %s WHERE Reg_No = %s"
                        cursor.execute(query, ("Admitted", app['Reg_No']))
                        conn.commit()
                        print("You have admitted this applicant!")
                        break
                    elif decision == "d":
                        query = f"UPDATE {applicant_table} SET status = 'Denied' WHERE Reg_No = {app['Reg_No']}"
                        cursor.execute(query)
                        conn.commit()
                        print("You have denied this applicant!")
                        break
                    else:
                        query = f"UPDATE {applicant_table} SET status = 'Waitlisted' WHERE Reg_No = {app['Reg_No']}"
                        cursor.execute(query)
                        conn.commit()
                        print("You have Waitlisted this applicant!")
                        break
                user_input = input("Press Enter to see the next applicant, or press 1 to exit app reviews: ")
                if user_input == "1":
                    if conn.is_connected():
                        conn.close()
                        return      
    except mysql.connector.Error as e:
        print(f" Database error: {e}")
        cursor.close()
    except KeyboardInterrupt:
        print("Exiting App reviews.....")
        time.sleep(1.5)
        cursor.close()
        return
    finally:
        if conn.is_connected():
            conn.close()
            cursor.close()

        util.clear_terminal()
        print("You have viewed all current applications")
        print("Redirecting back to login......")
        time.sleep(1.5)
        




def edit_profile(officer):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch existing data
        cursor.execute("SELECT * FROM officers WHERE email = %s", (officer.email,))
        officer_result = cursor.fetchone() #This is a dictionary
        cursor.execute(f"SELECT * FROM universities WHERE id = {officer.code}")
        university_result = cursor.fetchone() #This is a dictionary

        if not officer_result:
            print(f" No data found for {officer.name}")
            return
        if not university_result:
            print(f"No data found for {officer.university}")
            return

        print("\nLoading Profile Information...")
        time.sleep(1)
        util.clear_terminal()
        print("=" * 75)
        print(f"Details for {officer.name} of {officer.university}")
        print("=" * 75)

        print(f"Name: {officer.name}")
        new_name = input("Enter new name (or press Enter to keep current): ").strip()
        if new_name:
            cursor.execute("UPDATE officers SET name = %s WHERE email = %s", (new_name, officer.email))
            officer.name = new_name #updating the object's name property
            conn.commit()
            print(" name updated successfully.")
        else:
            print(" No changes made.")
        
        print("=" * 75)
        print(f"Email: {officer.email}")
        new_email = input("Enter new email (or press Enter to keep current): ").strip()
        if new_email:
            cursor.execute("UPDATE officers SET email = %s WHERE email = %s", (new_email, officer.email))
            officer.email = new_email #updating the object's email property
            conn.commit()
            print(f" Email updated successfully to {officer.email}.")
            print(f"Remember this email when logging in next time")
        else:
            print(" No changes made.")
        
        print("=" * 75)
        print(f"Password: {officer.password}")
        new_password = input("Enter new password (or press Enter to keep current): ").strip()
        if new_password:
            cursor.execute("UPDATE officers SET password = %s WHERE email = %s", (new_password, officer.email))
            officer.password = new_password #updating the object's password property
            conn.commit()
            print("password updated successfully.")
            print("Remember this password when logging in next time.")
        else:
            print(" No changes made.")

        print("=" * 75)
        print(f"Current University Application Portal: {university_result['portal_status']}")
        print("University Application Status Change")
        print("1. Open")
        print("2. Close")
        print("3. Press enter to make no change")
        new_status = input("Choose [1, 2, 3]: ").strip()
        if new_status == "1":
            cursor.execute(f"UPDATE universities SET portal_status = 'Open' WHERE id = {officer.code}")
            conn.commit()
            print(f" Portal status updated successfully to Open.")
        elif new_status == "2":
            cursor.execute(f"UPDATE universities SET portal_status = 'Closed' WHERE id = {officer.code}")
            conn.commit()
            print(f" Portal status updated successfully to Closed.")
        else:
            print(" No changes made.")

    except mysql.connector.Error as e:
        print(f" Database error: {e}")

    except KeyboardInterrupt:
        print("Exiting Profile Changes...")
        time.sleep(1.5)
        return
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
        input("\nPress Enter to return to the dashboard.")


if __name__ == "_main_":
    pass
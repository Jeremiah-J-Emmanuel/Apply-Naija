

def edit_general_info(name): print(f"Editing info for {name}..."); input("Press Enter to continue.")

def check_application_statuses(name): print(f"Checking application status for {name}..."); input("Press Enter to continue.")

def home_bar(name): print(f"This is {name}'s home bar..."); input("Press Enter to continue.")
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
    print('"Education 🏫 is the most powerful weapon which you can use to change the world."-Nelson Mandela')
    print(" Send in your univesity application, and get ready to change the world!")
    print("=" * 50)

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
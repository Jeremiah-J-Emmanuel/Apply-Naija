import os
import time
from student_func import (
    send_application,
    withdraw_application,
    edit_general_info,
    search_universities,
    check_application_status,
    home_bar
)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_student_env(student_name):
    while True:
        clear_terminal()
        print(f"\n🎓 Welcome {student_name}, to your dashboard!")
        print("=" * 50)
        print("1. Send an Application")
        print("2. Withdraw an Application")
        print("3. Edit General Information")
        print("4. Search for Universities")
        print("5. Check Application Status")
        print("6. Home Bar")
        print("7. Logout")
        print("=" * 50)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            send_application(student_name)
        elif choice == '2':
            withdraw_application(student_name)
        elif choice == '3':
            edit_general_info(student_name)
        elif choice == '4':
            search_universities()
        elif choice == '5':
            check_application_status(student_name)
        elif choice == '6':
            home_bar(student_name)
        elif choice == '7':
            print("\nLogging out...")
            time.sleep(1.5)
            break
        else:
            print("⚠️ Invalid input. Please enter a number from 1 to 7.")
            time.sleep(2)

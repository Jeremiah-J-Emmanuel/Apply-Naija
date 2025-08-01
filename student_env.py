#!/usr/bin/bash
import os
import time
from student_func import (
    send_or_withdraw,
    edit_general_info,
    search_bar,
    check_application_statuses,
    scholarship_list,
    home_bar
)
#function to clear the terminal screen for better readability.
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
#Main Student dashboard that helps students interact with the system
def load_student_env(student): #This function takes the student object as an argument
    while True:
        clear_terminal()
    #Welcome message and menu options.
        print(f"\n🎓 Welcome {student.name}, to your dashboard!")
        print("=" * 50)
        print("1. Send or withdraw an Application")
        print("2. See Scholarships")
        print("3. Edit General Information")
        print("4. Search for Universities")
        print("5. Check Application Status")
        print("6. Home Bar")
        print("7. Logout")
        print("=" * 50)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            send_or_withdraw(student)
        elif choice == '2':
            scholarship_list()
        elif choice == '3':
            edit_general_info(student)
        elif choice == '4':
            search_bar()
        elif choice == '5':
            check_application_statuses(student)
        elif choice == '6':
            home_bar(student)
        elif choice == '7':
            print("\nLogging out...")
            time.sleep(1.5)
            break
        else:
            print("⚠️ Invalid input. Please enter a number from 1 to 7.")
            time.sleep(1)

if __name__ == "__main__":
    load_student_env("Hoby")
# officer_env.py

import os
import time
from admin import review_app, edit_profile

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_officer_env(officer): #This function will take an object called officer
    while True:
        clear_terminal()
        print(f"\n🏛️ Welcome, {officer.name}, Admissions Officer for {officer.university}!")
        print("=" * 50)
        print("1. Review Applications")
        print("2. Edit University Profile Information")
        print("3. Logout")
        print("=" * 50)

        choice = input("Enter your choice (1–3): ").strip()

        if choice == '1':
            review_app(officer)
        elif choice == '2':
            edit_profile(officer)
        elif choice == '3':
            print("\nLogging out...")
            time.sleep(1.5)
            break
        else:
            print("⚠️ Invalid input. Please enter a number from 1 to 3.")
            time.sleep(1)


if __name__ == "__main__":
    load_officer_env()


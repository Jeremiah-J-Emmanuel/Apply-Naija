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
    # For quick testing only; remove before final submission
if __name__ == "__main__":
    scholarship_list()
    search_bar()
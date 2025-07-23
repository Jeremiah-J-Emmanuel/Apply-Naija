#Admin function for Apply-Naija
import mysql.connector

def connect_db():
    try: 
        connection = mysql.connector.connect(
            host='mysql-2008-alustudent-3086.f.aivencloud.com',
            port='15699',
            user='avnadmin',
            password='AVNS_1DzsuhCNrX8Dsvjg2wA',
            database='APPLY_NAIJA',
            ssl_disabled=False
        )
        print("Connection successful")
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def check_application_status(cursor, student_id, school_id):
    query = """
    SELECT * FROM applications 
    WHERE student_id = %s AND school_id = %s
    """
    cursor.execute(query, (student_id, school_id))
    return cursor.fetchone()

def process_application(cursor, student_id, school_id):
    query = """
    SELECT students.grade, schools.name 
    FROM students 
    JOIN applications ON students.id = applications.student_id 
    JOIN schools ON schools.id = applications.school_id 
    WHERE students.id = %s AND schools.id = %s
    """
    cursor.execute(query, (student_id, school_id))
    result = cursor.fetchone()
    
    if result:
        grade, school_name = result
        print(f"\n{school_name} Application Found: Grade = {grade}")
        
        if grade >= 70:
            decision = 'Admitted'
        elif grade >= 50:
            decision = 'Waitlisted'
        else:
            decision = 'Rejected'
        
        # Update application status
        update_query = """
        UPDATE applications SET status = %s 
        WHERE student_id = %s AND school_id = %s
        """
        cursor.execute(update_query, (decision, student_id, school_id))
        print(f"Decision: {decision}")
        return decision
    else:
        print("Application not found.")
        return None

def main():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        
        student_id = input("Enter student ID: ")
        school_id = input("Enter school ID: ")
        
        application = check_application_status(cursor, student_id, school_id)
        if application:
            print("Application found. Processing...")
            decision = process_application(cursor, student_id, school_id)
            conn.commit()
        else:
            print("No application found for this student and school.")
        
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='mysql-2008-alustudent-3086.f.aivencloud.com',
        port='15699',
        user='avnadmin',
        password='AVNS_1DzsuhCNrX8Dsvjg2wA',
        database='APPLY_NAIJA',
        ssl_disabled=False
    )

def review_app(university_name):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get the university ID
        cursor.execute("SELECT id FROM schools WHERE name = %s", (university_name,))
        result = cursor.fetchone()

        if not result:
            print(f" No university found with name {university_name}")
            return

        school_id = result['id']

        # Fetch student applications
        cursor.execute("""
            SELECT a.student_id, s.name, s.grade, a.status
            FROM applications a
            JOIN students s ON a.student_id = s.id
            WHERE a.school_id = %s
        """, (school_id,))
        applications = cursor.fetchall()

        if not applications:
            print(f" No applications for {university_name}")
        else:
            print(f"\n Applications for {university_name}:\n")
            for app in applications:
                print(f" {app['name']} (ID: {app['student_id']}) — Grade: {app['grade']} — Status: {app['status']}")

                # Automatically process grade (optional)
                if app['status'].lower() == 'pending':
                    grade = app['grade']
                    if grade >= 70:
                        decision = 'Admitted'
                    elif grade >= 50:
                        decision = 'Waitlisted'
                    else:
                        decision = 'Rejected'

                    # Update DB
                    cursor.execute("""
                        UPDATE applications
                        SET status = %s
                        WHERE student_id = %s AND school_id = %s
                    """, (decision, app['student_id'], school_id))
                    conn.commit()
                    print(f"  Application updated to: {decision}")

    except mysql.connector.Error as e:
        print(f" Database error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
        input("\nPress Enter to return to the dashboard.")

def edit_profile(university_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch existing data
        cursor.execute("SELECT id, location FROM schools WHERE name = %s", (university_name,))
        result = cursor.fetchone()

        if not result:
            print(f" No university found with name {university_name}")
            return

        school_id, current_location = result
        print(f"\n Current location of {university_name}: {current_location}")
        new_location = input("Enter new location (or press Enter to keep current): ").strip()

        if new_location:
            cursor.execute("UPDATE schools SET location = %s WHERE id = %s", (new_location, school_id))
            conn.commit()
            print(" Location updated successfully.")
        else:
            print(" No changes made.")

    except mysql.connector.Error as e:
        print(f" Database error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
        input("\nPress Enter to return to the dashboard.")

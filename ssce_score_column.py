
import mysql.connector

DB_CONFIG = {
    'host': 'mysql-2008-alustudent-3086.f.aivencloud.com',
    'port': 15699,
    'user': 'avnadmin',
    'password': 'AVNS_1DzsuhCNrX8Dsvjg2wA',
    'database': 'APPLY_NAIJA',
    'ssl_disabled': False
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Check if 'ssce_score' column already exists
    cursor.execute("SHOW COLUMNS FROM students LIKE 'ssce_score';")
    result = cursor.fetchone()

    if result:
        print("⚠️ 'ssce_score' column already exists.")
    else:
        cursor.execute("ALTER TABLE students ADD COLUMN ssce_score INT;")
        conn.commit()
        print("✅ 'ssce_score' column added successfully.")

    # Show all columns in the students table
    print("\n📋 Columns in 'students' table:")
    cursor.execute("SHOW COLUMNS FROM students;")
    for column in cursor.fetchall():
        print(f"- {column[0]} ({column[1]})")

except mysql.connector.Error as e:
    print(f"❌ Error: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()

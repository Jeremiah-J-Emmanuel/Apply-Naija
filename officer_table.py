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
    cursor.execute("ALTER TABLE officers ADD COLUMN university_name VARCHAR(255);")
    conn.commit()
    print("✅ 'university_name' column added to officers table.")
except mysql.connector.Error as e:
    if e.errno == 1060:
        print("⚠️ Column 'university_name' already exists.")
    else:
        print(f"❌ Database Error: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()

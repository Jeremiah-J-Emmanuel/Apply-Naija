import mysql.connector
try:
    connection = mysql.connector.connect(
    host = 'mysql-2008-alustudent-3086.f.aivencloud.com',
    port = '15699',
    user = 'avnadmin',
    password = 'AVNS_1DzsuhCNrX8Dsvjg2wA',
    database = 'APPLY_NAIJA',
    ssl_disabled = False
    )
    
    
    print ("connection succesful")
except mysql.connector.Error as e:
    print(f"Error: {e}")
    
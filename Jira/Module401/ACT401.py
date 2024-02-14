import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="cap_evidence"
)
cursor = conn.cursor()

# Execute the SQL query to retrieve all cases
cursor.execute('SELECT * FROM evidence')

# Fetch all the results
all_cases = cursor.fetchall()

# Print or process the retrieved cases
for case in all_cases:
    print(case)

# Close the database connection
conn.close()
import dbsecrets
import mysql.connector

# constants for name strings
DATABASE_NAME = "creditcard_capstone"
BRANCH_TABLE = "CDW_SAPP_BRANCH"
CC_TABLE = "CDW_SAPP_CREDIT_CARD"
# CUSTOMER_TABLE = "CDW_SAPP_CUSTOMER"
CUSTOMER_TABLE = "customers"

# set up db connection
# db secrets might need to change
# ask team for name of module
try:
    connection = mysql.connector.connect(
        host="localhost",           
        user=dbsecrets.mysql_username,
        password=dbsecrets.mysql_password      
    )
except mysql.connector.Error as ex:
    print(ex)

# verify connection
if connection.is_connected():
    print("Connected to MySQL database!")
else:
    print("Failed to connect to MySQL database.")

# close the connection
connection.close()



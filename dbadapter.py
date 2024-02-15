import dbsecrets as secrets
import mysql.connector

# constants for name strings
DATABASE_NAME = "creditcard_capstone"

# table name constants
BRANCH_TABLE = "CDW_SAPP_BRANCH"
CC_TABLE = "CDW_SAPP_CREDIT_CARD"
CUSTOMER_TABLE = "CDW_SAPP_CUSTOMER"


class DataAdapter:
    def __init__(self):
        self.connection = \
            mysql.connector.connect(
                host="localhost",           
                user=secrets.mysql_username,
                password=secrets.mysql_password)
        self.database_name = DATABASE_NAME

    def create_database(self):
        cursor = self.connection.cursor(buffered=True)
        command = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
        cursor.execute(command)
        cursor.close()

    def create_tables(self):
        # create customers table

        # create branches table

        # create transactions table
        pass

    def get_all_customers(self):
        command = f"SELECT * FROM {CUSTOMER_TABLE}"
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(command)
        results = cursor.fetchall()
        return results
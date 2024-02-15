import build_database as db

class DataAdapter:
    def __init__(self,connection):
        self.connection = connection


    def get_all_customers(self):
        command = f"SELECT * FROM {db.CUSTOMER_TABLE}"
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(command)
        results = cursor.fetchall()
        return results
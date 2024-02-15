from dbadapter import DataAdapter as DataAdapter
import mysql.connector
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",           
    user="root",
    password="password",
    database="classicmodels"      
)

dataAdapter = DataAdapter(connection)

customers = pd.DataFrame(dataAdapter.get_all_customers())

print(customers)
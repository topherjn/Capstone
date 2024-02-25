import calendar as cal
from os import system, name
import dbadapter as db
import dbsecrets as secret
import constants as const
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import findspark
findspark.init()

def print_pretty_details(df):
    row_rdd = df.rdd
    first_row = row_rdd.first()

    # Iterate through column names and values and print them
    for i, col_name in enumerate(df.columns):
        print(f"{col_name}: {first_row[i]}")



def get_customer_details(cust_id):
    cust_id = "123451007"

    spark = SparkSession.builder.appName('capstone json').getOrCreate()
    
    df = spark.read.format("jdbc") \
        .option("driver",const.DB_DRIVER) \
        .option("url", f"{const.DB_URL}/{const.DATABASE_NAME}") \
        .option("dbtable",const.CUSTOMER_TABLE) \
        .option("user", secret.mysql_username ) \
        .option("password", secret.mysql_password) \
        .load()
    
    df = df.where(col("ssn")==cust_id)

    return df
    
    # Functional Requirements 2.2

    # Rubric: - (9%)
    # 1) Used to check the existing account details of a customer.
    # 2) Used to modify the existing account details of a customer. 

    # 4) Used to display the transactions made by a customer between two
    # dates. Order by year, month, and day in descending order.
    def display_transactions_by_dates(cust_id,begin, end):
        pass

if __name__ == "__main__":
    df = get_customer_details(24234)
    if df.rdd.isEmpty():
        print("Customer doesn't exist")
    else:
        print_pretty_details(df)

# 1) Used to check the existing account details of a customer.
# 2) Used to modify the existing account details of a customer.
# 3) Used to generate a monthly bill for a credit card number for a given
# month and year.
# Hint: What does YOUR monthly credit card bill look like? What structural
# components does it have? Not just a total $ for the month, right?
# 4) Used to display the transactions made by a customer between two
# dates. Order by year, month, and day in descending order.
'''select *
from cdw_sapp_customer c inner join cdw_sapp_credit_card t on c.ssn = t.CUST_SSN
where t.CUST_SSN = "123451007" and t.TIMEID between 20180115 and 20180530
order by t.timeid desc;'''

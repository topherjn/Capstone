import calendar as cal
from os import system, name
import dbadapter as db
import dbsecrets as secret
import constants as const
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import findspark
findspark.init()

findspark.init()
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

    df.show()
    

    
    # Functional Requirements 2.2

    # Rubric: - (9%)
    # 1) Used to check the existing account details of a customer.
    # 2) Used to modify the existing account details of a customer. 

    # 4) Used to display the transactions made by a customer between two
    # dates. Order by year, month, and day in descending order.

if __name__ == "__main__":
    get_customer_details(24234)
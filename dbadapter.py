import findspark
from pyspark.sql import SparkSession
import mysql.connector
import constants as const
import dbsecrets as secrets

findspark.init()


class DataAdapter:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user=secrets.mysql_username,
            passwd=secrets.mysql_password,
        )

        self.session_properties = {
            'user': secrets.mysql_username,
            'password': secrets.mysql_password,
            'host': const.DB_URL,
            'driver': 'com.mysql.jdbc.Driver',
            'database': const.DATABASE_NAME
        }

        self.session = SparkSession \
            .builder \
            .appName("capstone") \
            .master("local[*]") \
            .getOrCreate()

        self.session.sparkContext.setLogLevel("ERROR")

        self.database_name = const.DATABASE_NAME

    def get_config_info(self):
        config = self.session.sparkContext.getConf().getAll()
        for item in config:
            print(item)

    def create_database(self):
        # cursor = self.connection.cursor(buffered=True)
        # command = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
        # cursor.execute(command)
        # cursor.close()
        command = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
        cursor = self.conn.cursor()
        # Create database
        cursor.execute(command)

    # create a mysql table from a Spark dataframe
    def create_table(self, df, table_name):
        # print(f"{const.DB_URL}/{self.database_name}")
        df.write.format("jdbc") \
            .mode("overwrite") \
            .option("url", f"{const.DB_URL}/{self.database_name}") \
            .option("dbtable", table_name) \
            .option("user", secrets.mysql_username) \
            .option("driver", "com.mysql.jdbc.Driver") \
            .option("password", secrets.mysql_password) \
            .save()

    # return a Spark dataframe from a mysql table
    # for customers in classicmodels
    def get_all_customers(self):
        df = (self.session.read
              .format("jdbc")
              .option("url",  f"{const.DB_URL}/{self.database_name}")
              .option("dbname", "classicmodels")
              .option("user", self.session_properties["user"])
              .option("password", self.session_properties["password"])
              .option("dbtable", "customers")
              .load())

        df.show()

    # 2.1.3- Use the provided inputs to query the database and retrieve a list of transactions made by customers in the
    # specified zip code for the given month and year.
    # 2.1.4 - Sort the transactions by day in descending order.    
    def get_specified_transactions(self, zip_code: object, month: object, year: object):
        df = (self.session.read.format("jdbc")
              .option("driver","com.mysql.jdbc.Driver")
              .option("url","jdbc:mysql://localhost:3306/creditcard_capstone")
              .option("dbtable","(select branch_code from creditcard_capstone.cdw_sapp_branch) as sql")
              .option("user", secrets.mysql_username).option("password", secrets.mysql_password)
              .load())

        df.show()



    # 1) Used to check the existing account details of a customer.
    def get_customer_details(self, ssn):
        pass

    # 2) Used to modify the existing account details of a customer.
    # get all details in a data object, change, then save whole thing back
    def update_customer_details(self, ssn):
        # details = self.get_customer_details(self, ssn)
        pass

    # 3) Used to generate a monthly bill for a credit card number for a given month and year.
    # Hint: What does YOUR monthly credit card bill look like?  What structural components 
    # does it have?  Not just a total $ for the month, right?

    def generate_customer_bill(self, snn):
        pass

    # 4) Used to display the transactions made by a customer between two dates.
    # Order by year, month, and day in descending order.
    def generate_transaction_report(self, snn, start, end):
        pass

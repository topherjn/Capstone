import constants as const
import dbsecrets as secrets
import findspark
findspark.init()

from pyspark.sql import SparkSession


class DataAdapter:
    def __init__(self):

        self.connection = SparkSession \
                          .builder \
                          .appName("capstone") \
                          .master("local[*]") \
                          .getOrCreate()
        
        self.connection.sparkContext.setLogLevel("ERROR")
        
        self.database_name = const.DATABASE_NAME

    def get_config_info(self):
        config=self.connection.sparkContext.getConf().getAll()
        for item in config:
            print(item)

    def create_database(self):
        # cursor = self.connection.cursor(buffered=True)
        # command = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
        # cursor.execute(command)
        # cursor.close()
        command = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"

       
        

    def create_tables(self):
        # create customers table

        # create branches table

        # create transactions table
        pass

    def get_all_customers(self):
        # command = f"SELECT * FROM {CUSTOMER_TABLE}"
        # cursor = self.connection.cursor(buffered=True)
        # cursor.execute(command)
        # results = cursor.fetchall()
        query="(select * from customers) as cust"

        df = self.connection.read.format("jdbc").options(driver="com.mysql.cj.jdbc.Driver",\
                                     user="root",\
                                     password="password",\
                                     url="jdbc:mysql://localhost:3306/classicmodels",\
                                     dbtable=query).load()
        
        df.show()

    # 2.1.3- Use the provided inputs to query the database and retrieve a list of transactions made by customers in the specified zip code for the given month and year.
    # 2.1.4 - Sort the transactions by day in descending order.    
    def get_specified_transactions(self,zip_code, month, year):
        return zip_code, month, year
    
    # 1) Used to check the existing account details of a customer.
    def get_customer_details(self,ssn):
        pass

    # 2) Used to modify the existing account details of a customer.
    # get all details in a data object, change, then save whole thing back
    def update_customer_details(self,ssn):
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
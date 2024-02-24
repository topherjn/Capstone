import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import mysql.connector
import constants as const
import dbsecrets as secrets

findspark.init()

# this class handles all MySQL RDBMS tasks and some PySpark tasks
# dealing with reading and writing data
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
            'driver': 'const.DB_DRIVER',
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
        command = f"DROP DATABASE IF EXISTS {self.database_name}"
        cursor = self.conn.cursor()
        # Create database
        cursor.execute(command)
        
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
            .option("driver", const.DB_DRIVER) \
            .option("password", secrets.mysql_password) \
            .save()
        
    def add_keys(self):

        # add primary keys
        cursor = self.conn.cursor()
        cursor.execute(f"use {const.DATABASE_NAME}")
        command = f"alter table {const.CUSTOMER_TABLE} add primary key (ssn)"
        cursor.execute(command)
        command = (f"alter table {const.BRANCH_TABLE} add primary key (branch_code)")
        cursor.execute(command)
        command = (f"alter table {const.CC_TABLE} add primary key (transaction_id)")

        cursor.execute(command)

        # add foreign keys
        command = (f"alter table {const.CC_TABLE} \
                          add constraint fk_branch \
                          foreign key (branch_code) references \
                          {const.BRANCH_TABLE}(branch_code)")
        
        cursor.execute(command)

        command = (f"alter table {const.CC_TABLE} \
                     add constraint fk_cust \
                     foreign key (cust_ssn) references \
                     {const.CUSTOMER_TABLE}(ssn)")
        
        cursor.execute(command)

        cursor.close()

    # return a Spark dataframe from a mysql table
    # for customers in classicmodels

    def get_table_data(self, table):
     
        df=self.session.read.format("jdbc").options(driver=const.DB_DRIVER,\
                                            user=secrets.mysql_username,\
                                            password=secrets.mysql_password,\
                                            url= f"{const.DB_URL}/{const.DATABASE_NAME}", \
                                            dbtable=table).load()
        return df

    # 2.1.3- Use the provided inputs to query the database and retrieve a list of transactions made by customers in the
    # specified zip code for the given month and year.
    # 2.1.4 - Sort the transactions by day in descending order.    
    def get_specified_transactions(self, zip_code: object, month: object, year: object):
        
        # get credit-card table from RDBMS
        transaction_df=self.get_table_data(const.CC_TABLE)
        
        # get customer table from RDBMS
        customer_df = self.get_table_data(const.CUSTOMER_TABLE)

        # get branch table from RDBMS
        branch_df= self.get_table_data(const.BRANCH_TABLE)
        
        # join the three tables
        combined_df = customer_df.join(transaction_df, on='CREDIT_CARD_NO')
        combined_df = combined_df.join(branch_df, on='BRANCH_CODE')

        # apply the selection criteria to the join
        combined_df = combined_df \
                            .where(  (col("TIMEID")
                            .substr(0,6) == str(year)+str(month)
                            .rjust(2,'0')) & (col("CUST_ZIP")==str(zip_code)
                            .rjust(5,'0')))
        
        # sort
        combined_df = combined_df.sort("TIMEID",ascending=False)

        # display the results
        # TODO make legible
        combined_df.show()
       

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

    def close(self):
        self.session.stop()

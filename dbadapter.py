import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import mysql.connector
import constants as const
import dbsecrets as secrets
import utils as ut

findspark.init()

# this class handles all MySQL RDBMS tasks and some PySpark tasks
# dealing with reading and writing data
class DataAdapter:
    # constructor sets up MySQL and Spark connectors
    def __init__(self):

        # data adapter has its own MySQL connector
        self.conn = mysql.connector.connect(
            host="localhost",
            user=secrets.mysql_username,
            passwd=secrets.mysql_password,
        )

        # has its own pyspark session
        self.session = SparkSession \
            .builder \
            .appName("capstone") \
            .master("local[*]") \
            .getOrCreate()

        # store the main MySQL database here, probably not
        # needed
        self.database_name = const.DATABASE_NAME

    # create the capstone db
    def create_database(self):
        command = f"DROP DATABASE IF EXISTS {self.database_name}"
        cursor = self.conn.cursor()

        # Create database
        cursor.execute(command)
        
        command = f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
        cursor = self.conn.cursor()
        # Create database
        cursor.execute(command)

        cursor.close()

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
    
    # convert Spark types to MySQL types
    def map_data_types(self):

        # don't have Spark 3.5.0 so no access to MySQl types
        # first get a list of table names
        # the a list of column names for each table
        # default is varchar
        # then change specific ones
        cursor = self.conn.cursor()

        command = "SELECT table_name,column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS where table_schema = 'creditcard_capstone'"
        cursor.execute(command)
        columns = cursor.fetchall()
        
        command = f"USE {const.DATABASE_NAME}"
        cursor.execute(command)
        for column in columns:
            data_type = ''
            if column[2] in ["bigint","text"]:
                if column[1] == "LAST_UPDATED":
                    data_type = "TIMESTAMP"
                elif column[2] == 'bigint':
                    data_type = 'int'
                elif column[2] == 'text':
                    data_type = 'varchar(255)'

                command = f"alter table {column[0]} modify {column[1]} {data_type}"

                #print(command)
                cursor.execute(command)
            
        cursor.close()
        
    # create MySQL relationships
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

        # add foreign keys - credit card table is the junction
        # from credit card to branch
        command = (f"alter table {const.CC_TABLE} \
                          add constraint fk_branch \
                          foreign key (branch_code) references \
                          {const.BRANCH_TABLE}(branch_code)")
        
        cursor.execute(command)

        # from credit card to customer
        command = (f"alter table {const.CC_TABLE} \
                     add constraint fk_cust \
                     foreign key (cust_ssn) references \
                     {const.CUSTOMER_TABLE}(ssn)")
        
        cursor.execute(command)

        cursor.close()

    # return a Spark dataframe from a mysql table
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
        # TODO make legible?
        combined_df.show()
       
    # 1) Used to check the existing account details of a customer.
    def get_customer_details(self, ssn):
        df = self.get_table_data(const.CUSTOMER_TABLE)
        df = df.where(col("SSN") == ssn)
        return df

    # 2) Used to modify the existing account details of a customer.
    def update_customer_record(self, field, val, ssn):

        cursor = self.conn.cursor()
        cursor.execute(f"use {const.DATABASE_NAME}")

        command = f"UPDATE {const.CUSTOMER_TABLE} SET {field}='{val}',LAST_UPDATED=NOW() WHERE SSN='{ssn}'"
        # print(command) for debugging
        cursor.execute(command)
        cursor.close()
        self.conn.commit()

    # before you change details you read them
    # creates an update statement from user interaction
    def update_customer_details(self, ssn):
        details = self.get_customer_details(ssn)
        # only try to get details on existing customers
        if not details.rdd.isEmpty():
            details = details.select('FIRST_NAME','MIDDLE_NAME','LAST_NAME',
                                    'FULL_STREET_ADDRESS','CUST_CITY','CUST_STATE',
                                    'CUST_COUNTRY','CUST_ZIP','CUST_PHONE')
            print("Current values:")
            details.show()

            fields = details.columns
            fields.append('quit')

            # since this is a console app using an option interaction loop
            # to allow changing multiple values, but only one at a time
            print("Which of the above fields would you like to update?")
            field = input("Please type the exact column name: ")
            print(field)

            while field.lower() != 'quit':

                while not field.lower() in fields:
                    print("Try again.")
                    field = input("Please type the exact column name or 'quit': ")
                    print(field)

                if field.lower() != 'quit':
                    field = field.lower()
                    
                    val = input("What value do you want to change the field to? ")
                    self.update_customer_record(field=field,val=val, ssn=ssn)

                print("Which of the above fields would you like to update?")
                field = input("Please type the exact column name or 'quit': ")
                print(field)
        else: 
            print(f"Customer {ssn} does not exist.")

    # 3) Used to generate a monthly bill for a credit card number for a given month and year.
    # Hint: What does YOUR monthly credit card bill look like?  What structural components 
    # does it have?  Not just a total $ for the month, right?
    def generate_cc_bill(self, ccn, month, year):
        # construct where clause value (by time)
        timeid = ut.make_timeid(year,month,0) + "%"

        # in order just to get customer name we have to join
        df = self.get_table_data(const.CC_TABLE)

        # names for join on not same so rename one
        df = df.withColumnRenamed('CUST_SSN','SSN')
        cust_df = self.get_table_data(const.CUSTOMER_TABLE)
        cust_df = cust_df.select('SSN','FIRST_NAME','LAST_NAME')
        
        # the join
        df=df.join(cust_df,on ='SSN')
        df = df.where(col('CREDIT_CARD_NO')==ccn)
        df = df.where(col('TIMEID').like(timeid))
        
        # if the user is looking for something that doesn't exist
        # then this part is skipped.  Save on typos and other
        # user-input gibberish too
        if not df.rdd.isEmpty():
            print(f"Transaction summary for credit card number: {ccn}\nFor customer:")
            df.select('FIRST_NAME','LAST_NAME').distinct().show()

            # print out a summary for the month
            print(f"Activity for {month} {year}:")
            df.select("TIMEID","TRANSACTION_TYPE","TRANSACTION_VALUE").show()

            # total bill for the month
            print("Total charges")
            total_charges = df.agg({"TRANSACTION_VALUE":"sum"}).collect()[0]
            print(round(float(total_charges['sum(TRANSACTION_VALUE)']),2))
        else:
            print("No results")
        
    # 4) Used to display the transactions made by a customer between two dates.
    # Order by year, month, and day in descending order.
    def generate_transaction_report(self, ssn, start, end):
        df = self.get_table_data(const.CC_TABLE)
        df = df.where(col("CUST_SSN")==ssn)
        df = df.where(col("TIMEID").between(start,end))
        df.collect()
        df = df.sort("TIMEID",ascending=False)
        df.show()

    # this returns transaction totals by 'transaction type'
    def get_transaction_totals_by_category(self, category):
        df = self.get_table_data(const.CC_TABLE)
        categories = []
        for item in df.select('TRANSACTION_TYPE').distinct().collect():
            categories.append(item[0].lower())

        # will not crash on nonsense categories
        if category.lower() in categories:
            df = df.where(col("TRANSACTION_TYPE") == category)
            count = df.count()
            total = df.agg({"TRANSACTION_VALUE":"sum"}).collect()[0]
            print(f"Total value of {count} transactions in category {category}: ")
            print(round(float(total['sum(TRANSACTION_VALUE)']),2))
        else:
            print(f"No such category {category} in {categories} ")

    # one branch per city, so using that to calculate 
    # transaction totals
    def get_transaction_totals_by_branch(self):
        df = self.get_table_data(const.BRANCH_TABLE)
        df = df.select("BRANCH_CITY","BRANCH_CODE")
        
        cities = []
        for item in df.select('BRANCH_CITY').collect():
            cities.append(item[0].lower())
        
        df = df.join(self.get_table_data(const.CC_TABLE), on='BRANCH_CODE')
        city = input("Enter branch city for transaction totals: ")
        city = city.lower()
        
        # this error-checks input for branches that don't exist
        if city in cities:
            df = df.where(col('BRANCH_CITY') == city)
            count = df.count()
            total = df.agg({"TRANSACTION_VALUE":"sum"}).collect()[0]
            print(f"Total value of {count} transactions from {city} branch: ")
            print(round(float(total['sum(TRANSACTION_VALUE)']),2))
        else: 
            print(f"No branch in {city}")
        
    def close(self):
        self.session.stop()

if __name__ == "__main__":
    '''testing statements'''
    # data_adapter = DataAdapter()

    # data_adapter.get_specified_transactions('55044', '02', '2018')

    # data_adapter.close()

    data_adapter = DataAdapter()

    data_adapter.generate_cc_bill('4210653349028689','01','2018')
    # #data_adapter.update_customer_details(123451152)
    # data_adapter.get_transaction_totals_by_category("gfdsafAs")


    # data_adapter.generate_transaction_report(123451152,20180101,20180415)
    
    data_adapter.close()

    

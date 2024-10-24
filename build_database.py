import constants as const
from dbadapter import DataAdapter
from pyspark.sql.functions import col, lower, concat, lit, initcap, lpad, regexp_replace
from pyspark.sql.types import StringType
import cdw_data_reader as cdr
import load_loan_data as lld
from os.path import isfile


def build_database():
    # create data adapter
    data_adapter = DataAdapter()

    # create database
    print("Creating database ...")
    data_adapter.create_database()

    # # create tables
    # customers
    print("Cleaning customers data ...")
    cust_df = cdr.get_dataframe(const.CUSTOMER_FILE)

    # convert middle name to lower case
    cust_df = cust_df.withColumn("MIDDLE_NAME",lower(col("MIDDLE_NAME")))

    # Concatenate Apartment no and Street name of customer's Residence with comma as a seperator (Street, Apartment)
    cust_df = cust_df.withColumn("APT_NO", concat(col("APT_NO"), lit(","), col("STREET_NAME")))
    cust_df = cust_df.withColumnRenamed("APT_NO","FULL_STREET_ADDRESS")
    cust_df = cust_df.drop("STREET_NAME")

    # Convert the First and Last Name to Title Case
    cust_df = cust_df.withColumn("FIRST_NAME",initcap(col("FIRST_NAME")))
    cust_df = cust_df.withColumn("LAST_NAME",initcap(col("LAST_NAME")))

    # Change the format of phone number to (XXX)XXX-XXXX
    cust_df = cust_df.withColumn("CUST_PHONE",cust_df["CUST_PHONE"].cast(StringType()))
    cust_df = cust_df.withColumn("CUST_PHONE",
                                 concat(lit("(000)"),
                                 col("CUST_PHONE")[0:3],
                                 lit("-"),
                                 col("CUST_PHONE")[4:7]))
    # pad zip
    cust_df = cust_df.withColumn("CUST_ZIP",lpad("CUST_ZIP",5,"0"))
    
    # branches
    print("Cleaning branches data ...")
    branch_df = cdr.get_dataframe(const.BRANCH_FILE)

    # handle zip nulls with default 99999
    branch_df = branch_df.fillna(99999,subset=['BRANCH_ZIP'])

    # Change the format of phone number to (XXX)XXX-XXXX
    branch_df = branch_df.withColumn("BRANCH_PHONE",branch_df["BRANCH_PHONE"].cast(StringType()))
    branch_df = branch_df.withColumn("BRANCH_PHONE",regexp_replace("BRANCH_PHONE", "(\\d{3})(\\d{3})(\\d{4})", "\($1\)$2-$3"))
    
    # pad zip
    branch_df = branch_df.withColumn("BRANCH_ZIP",lpad("BRANCH_ZIP",5,"0"))
    
    # # transactions
    print("Cleaning transactions data ...")
    transactions_df = cdr.get_dataframe(const.CREDIT_FILE)

    # pad month and day
    transactions_df = transactions_df.withColumn("MONTH",lpad("MONTH",2,"0"))
    transactions_df = transactions_df.withColumn("DAY",lpad("DAY",2,"0"))

    # create TIMEID column and remove redundant time columns
    transactions_df = transactions_df.withColumn("YEAR",concat(col("YEAR"),col("MONTH"),col("DAY")))
    transactions_df = transactions_df.withColumnRenamed("YEAR","TIMEID")
    transactions_df = transactions_df.drop("MONTH")
    transactions_df = transactions_df.drop("DAY")

    # cache the loan data from the REST api
    # but grab it if it's missing
    if isfile(f"data\{const.LOAN_FILE}"):
        # local json
        print("Fetching local cache of loan data ...")
        loan_df = cdr.get_dataframe(const.LOAN_FILE)
    else: 
        # online json
        print("Fetching online loan data ...")
        loan_json_data = lld.main_request(const.LOAN_URL)
        loan_df = cdr.get_dataframe(str(loan_json_data), False)
        # cache it:
        print("... and caching it.")
        with open(f"data\{const.LOAN_FILE}", 'w') as f:
            f.write(loan_json_data)
   
    # create the tables in MySQL
    print("Creating tables in MySQL RDBMS")
    data_adapter.create_table(cust_df,const.CUSTOMER_TABLE)
    data_adapter.create_table(branch_df,const.BRANCH_TABLE)
    data_adapter.create_table(transactions_df,const.CC_TABLE)
    data_adapter.create_table(loan_df, const.LOAN_TABLE)

    # map data types - kludge
    # this uses the data adapter to convert inferred pyspark
    # data types to the required MySQL data types
    data_adapter.map_data_types()

    # create keys - primary and foreign
    data_adapter.add_keys()

    # free-up resources
    data_adapter.close()

if __name__ == "__main__":
    # test build database
    build_database()

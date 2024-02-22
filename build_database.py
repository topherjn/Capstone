import constants as const
from dbadapter import DataAdapter
from pyspark.sql.functions import col, lower, concat, lit, initcap, lpad
from pyspark.sql.types import StringType
import cdw_data_reader as cdr
import load_loan_data as lld


def build_database():
    # create data adapter
    data_adapter = DataAdapter()

    # data_adapter.get_config_info()

    # # create database
    print("Creating database ...")
    data_adapter.create_database()

    # # create tables
    # customers
    print("Creating customers table ...")
    cust_df = cdr.get_dataframe(const.CUSTOMER_FILE)
    # convert middle name to lower case
    cust_df = cust_df.withColumn("MIDDLE_NAME",lower(col("MIDDLE_NAME")))
    # Concatenate Apartment no and Street name of customer's Residence with comma as a seperator (Street, Apartment)
    cust_df = cust_df.withColumn("APT_NO", concat(col("APT_NO"), lit(","), col("STREET_NAME")))
    cust_df = cust_df.withColumnRenamed("APT_NO","FULL_STREET_ADDRESS")
    cust_df.drop("STREET_NAME")
    # Convert the First and Last Name to Title Case
    cust_df = cust_df.withColumn("FIRST_NAME",initcap(col("FIRST_NAME")))
    cust_df = cust_df.withColumn("LAST_NAME",initcap(col("LAST_NAME")))
    # Change the format of phone number to (XXX)XXX-XXXX
    cust_df = cust_df.withColumn("CUST_PHONE",cust_df["CUST_PHONE"].cast(StringType()))
    cust_df = cust_df.withColumn("CUST_PHONE",
                                 concat(lit("(000)"),
                                 col("CUST_PHONE")[0:3],
                                 lit("-"),
                                 col("CUST_PHONE")[4:8]))
    # pad zip
    cust_df = cust_df.withColumn("CUST_ZIP",lpad("CUST_ZIP",5,"0"))
    
    # # branches
    print("Creating branches table ...")
    branch_df = cdr.get_dataframe(const.BRANCH_FILE)

    # handle zip nulls with default 99999
    branch_df = branch_df.fillna(99999,subset=['BRANCH_ZIP'])

    # Change the format of phone number to (XXX)XXX-XXXX
    branch_df = branch_df.withColumn("BRANCH_PHONE",
                                 concat(lit("(000)"),
                                 col("BRANCH_PHONE")[0:3],
                                 lit("-"),
                                 col("BRANCH_PHONE")[4:8]))
    

    # # transactions
    print("Creating transactions table ...")
    transactions_df = cdr.get_dataframe(const.CREDIT_FILE)

    # online json
    # print("Creating loan application table ...")
    # loan_json_data = lld.main_request(const.LOAN_URL)
    # df = cdr.get_dataframe(str(loan_json_data), False)
   
    # create the tables in MySQL
    data_adapter.create_table(cust_df,const.CUSTOMER_TABLE)
    data_adapter.create_table(branch_df,const.BRANCH_TABLE)
    data_adapter.create_table(transactions_df,const.CC_TABLE)
     # data_adapter.create_table(df, const.LOAN_TABLE)

    data_adapter.close()

if __name__ == "__main__":
    # customer_data = dr.get_dataframe(const.CUSTOMER_FILE)
    # branch_data = dr.get_dataframe(const.BRANCH_FILE)
    # translation_data = dr.get_dataframe(const.CREDIT_FILE)

    # build database
    build_database()

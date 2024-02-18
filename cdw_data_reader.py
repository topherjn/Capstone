
import numpy as np
import filenames as fn
import findspark
findspark.init()
from pyspark.sql import SparkSession

JSON_FORMAT = """org.apache.spark.sql.json"""

def get_dataframe(data_file):

    data_folder = 'data'

    # one JSON object per line in file
    spark = SparkSession.builder.appName('capston').getOrCreate()

    df = spark.read.format(JSON_FORMAT).load(f"{data_folder}/{data_file}")
    return df

if __name__ == "__main__":

    branch_df = get_dataframe(fn.BRANCH_FILE)
    credit_df = get_dataframe(fn.CREDIT_FILE)
    customer_df = get_dataframe(fn.CUSTOMER_FILE)

    customer_df.show()


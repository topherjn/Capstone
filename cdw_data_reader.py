import constants as const
from pyspark.sql import SparkSession
import findspark
findspark.init()


JSON_FORMAT = """org.apache.spark.sql.json"""


def get_dataframe(data_file):
    data_folder = 'data'

    # one JSON object per line in file
    spark = SparkSession.builder.appName('capstone json').getOrCreate()

    df = spark.read.format(JSON_FORMAT).load(f'{data_folder}/{data_file}')

    return df


if __name__ == "__main__":
    branch_df = get_dataframe(const.BRANCH_FILE)
    credit_df = get_dataframe(const.CREDIT_FILE)
    customer_df = get_dataframe(const.CUSTOMER_FILE)

    df = (branch_df.join(credit_df).join(customer_df).
          where(branch_df['BRANCH_ZIP']=='55044').
          where(credit_df['MONTH']==1).
          where(credit_df['YEAR']==2018))

    df.show()


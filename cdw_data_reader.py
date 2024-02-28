import constants as const
from pyspark.sql import SparkSession
import findspark
findspark.init()

# input: json file output: spark dataframe
def get_dataframe(data_file,is_file=True):
    data_folder = 'data'

    # one JSON object per line in file
    spark = SparkSession.builder.appName('capstone json').getOrCreate()
    
    # this differentiates between the REST files and the local files
    if is_file:
        df = spark.read.format(const.JSON_FORMAT).load(f'{data_folder}/{data_file}')
    else:
        json_rdd = spark.sparkContext.parallelize([data_file])
        df = spark.read.json(json_rdd)

    return df


if __name__ == "__main__":
    pass



import constants as const
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
import findspark
findspark.init()

# input: json file output: spark dataframe
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

def get_dataframe(data_file, is_file=True):
    data_folder = 'data'

    try:
        spark = SparkSession.builder.appName('capstone json').getOrCreate()
        
        # commands are a little different between reading a local file
        # and reading from a Web service
        if is_file:
            df = spark.read.format(const.JSON_FORMAT).load(f'{data_folder}/{data_file}')
        else:
            json_rdd = spark.sparkContext.parallelize([data_file])
            df = spark.read.json(json_rdd)

        return df

    except AnalysisException as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    pass



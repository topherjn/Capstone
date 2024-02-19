from dbadapter import DataAdapter
import cdw_data_reader as dr
import constants as const

def build_database():
    # create data adapter
    data_adapter = DataAdapter()

    # create database
    data_adapter.create_database()

    # create tables
    data_adapter.create_tables()

    # load data

if __name__=="__main__":
    # get data first as pandas dataframes
    customer_data = dr.get_dataframe(const.CUSTOMER_FILE)
    branch_data = dr.get_dataframe(const.BRANCH_FILE)
    transation_data = dr.get_dataframe(const.CREDIT_FILE)


    # build database
    build_database()
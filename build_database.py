import constants as const
from dbadapter import DataAdapter
import cdw_data_reader as cdr
import load_loan_data as lld


def build_database():
    # create data adapter
    data_adapter = DataAdapter()

    # data_adapter.get_config_info()

    # # create database
    data_adapter.create_database()

    # # create tables
    # customers
    df = cdr.get_dataframe(const.CUSTOMER_FILE)
    data_adapter.create_table(df,const.CUSTOMER_TABLE)

    # branches
    df = cdr.get_dataframe(const.BRANCH_FILE)
    data_adapter.create_table(df,const.BRANCH_TABLE)

    # transactions
    df = cdr.get_dataframe((const.CREDIT_FILE))
    data_adapter.create_table(df,const.CC_TABLE)

    # online json

if __name__ == "__main__":
    # get data first as pandas dataframes
    # customer_data = dr.get_dataframe(const.CUSTOMER_FILE)
    # branch_data = dr.get_dataframe(const.BRANCH_FILE)
    # translation_data = dr.get_dataframe(const.CREDIT_FILE)

    # build database
    build_database()

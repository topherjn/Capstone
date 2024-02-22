import constants as const
from dbadapter import DataAdapter
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
    df = cdr.get_dataframe(const.CUSTOMER_FILE)
    data_adapter.create_table(df,const.CUSTOMER_TABLE)

    # # branches
    print("Creating branches table ...")
    df = cdr.get_dataframe(const.BRANCH_FILE)
    data_adapter.create_table(df,const.BRANCH_TABLE)

    # # transactions
    print("Creating transactions table ...")
    df = cdr.get_dataframe(const.CREDIT_FILE)
    data_adapter.create_table(df,const.CC_TABLE)

    # online json
    # print("Creating loan application table ...")
    # loan_json_data = lld.main_request(const.LOAN_URL)
    # df = cdr.get_dataframe(str(loan_json_data), False)
    # data_adapter.create_table(df, const.LOAN_TABLE)

    data_adapter.close()

if __name__ == "__main__":
    # customer_data = dr.get_dataframe(const.CUSTOMER_FILE)
    # branch_data = dr.get_dataframe(const.BRANCH_FILE)
    # translation_data = dr.get_dataframe(const.CREDIT_FILE)

    # build database
    build_database()

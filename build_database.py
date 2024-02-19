from dbadapter import DataAdapter


def build_database():
    # create data adapter
    data_adapter = DataAdapter()

    data_adapter.get_config_info()

    # # create database
    data_adapter.create_database()

    # # create tables
    # data_adapter.create_tables()

    # # load data
    data_adapter.get_all_customers()


if __name__ == "__main__":
    # get data first as pandas dataframes
    # customer_data = dr.get_dataframe(const.CUSTOMER_FILE)
    # branch_data = dr.get_dataframe(const.BRANCH_FILE)
    # translation_data = dr.get_dataframe(const.CREDIT_FILE)

    # build database
    build_database()

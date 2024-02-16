import pandas as pd
import numpy as np
import filenames as fn

def get_dataframe(data_file):

    data_folder = 'data'

    # one JSON object per line in file
    df = pd.read_json(f"{data_folder}/{data_file}", lines=True)
    
    return df

if __name__ == "__main__":

    branch_df = get_dataframe(fn.BRANCH_FILE)
    credit_df = get_dataframe(fn.CREDIT_FILE)
    customer_df = get_dataframe(fn.CUSTOMER_FILE)

    #https://stackoverflow.com/questions/33137686/python-loading-zip-codes-into-a-dataframe-as-strings
    branch_df['BRANCH_ZIP'] = branch_df['BRANCH_ZIP'].astype(str).str.zfill(5)

    # how to do a search by SSN
    print(customer_df[customer_df['SSN']==123454047])


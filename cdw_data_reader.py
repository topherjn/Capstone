import pandas as pd
import numpy as np

def get_dataframe(data_file):

    data_folder = 'data'

    # one JSON object per line in file
    df = pd.read_json(f"{data_folder}/{data_file}", lines=True)
    
    return df

if __name__ == "__main__":

    # make files names easier
    BRANCH_FILE = "cdw_sapp_branch.json"
    CREDIT_FILE = "cdw_sapp_branch.json"
    CUSTOMER_FILE = "cdw_sapp_custmer.json"

    branch_df = get_dataframe(BRANCH_FILE)
    credit_df = get_dataframe(CREDIT_FILE)
    customer_df = get_dataframe(CUSTOMER_FILE)

#https://stackoverflow.com/questions/33137686/python-loading-zip-codes-into-a-dataframe-as-strings
branch_df['BRANCH_ZIP'] = branch_df['BRANCH_ZIP'].astype(str).str.zfill(5)

print(branch_df)


import requests
import pandas as pd

url = "https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json"

def get_response_code(url):

    r = requests.get(url)

    code = r.status_code

    return code

def main_request(url):
    r = requests.get(url)

    return r

response = main_request(url)

if response.status_code == 200:
    print("Connection OK")

    contents = response.json()

    df = pd.json_normalize(contents)

    print(df)


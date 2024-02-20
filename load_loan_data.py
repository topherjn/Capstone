import requests
import constants as const
import pandas as pd

def get_response_code(url):

    r = requests.get(url)

    code = r.status_code

    return code

def main_request(url):
    r = requests.get(url)

    return r


import requests

def get_response_code(url):

    request = requests.get(url)

    code = request.status_code

    return code


def main_request(url):

    if get_response_code() == 200:
        request = requests.get(url)

    return request


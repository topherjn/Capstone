import requests

def get_response_code(url):

    request = requests.get(url)

    code = request.status_code

    return code


def main_request(url):
    request = None
    if get_response_code(url) == 200:
        request = requests.get(url)

    return request.text


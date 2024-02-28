import requests

# function to get the response code from HTTP
def get_response_code(url):

    request = requests.get(url)

    code = request.status_code

    return code

# get the response code
# if good then get the json data
def main_request(url):
    request = None
    if get_response_code(url) == 200:
        request = requests.get(url)

    return request.text


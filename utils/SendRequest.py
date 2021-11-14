import requests
from requests import RequestException


class SendRequest(object):
    all_result = dict
    list_data = list

    def __init__(self, url, header):
        self.url = url
        self.header = header

    def get_initial_data(self):
        try:
            response = requests.get(self.url, self.header)
            if response.status_code is 200:
                print(response.text)
                return response.text
            else:
                return None
        except RequestException:
            return None



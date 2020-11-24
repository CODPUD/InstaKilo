import requests
import json
import re
from datetime import datetime

class InstaKilo():

    API_URL = "https://www.instagram.com/"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        time = int(datetime.now().timestamp())
        csrf = self.get_csrf()

        headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
                "referer": self.API_URL + "accounts/login/",
                "x-csrftoken": csrf
        }

        payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        self.s = requests.Session()
        response = self.s.post(self.API_URL + "accounts/login/ajax/", data=payload, headers=headers)
        print(response)
        response = json.loads(response.text)
        print(response)

    def get_csrf(self):
        with requests.Session() as s:
            r = s.get(self.API_URL)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
        return csrf
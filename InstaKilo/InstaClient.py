import requests, pickle
import json
import re
from datetime import datetime
import bs4

class InstaKilo():

    API_URL = "https://www.instagram.com/"
    IGQ = API_URL + "graphql/query/"

    def __init__(self, username, password):
        #User Data
        self.username = username
        self.password = password

        self.csrf = self.get_csrf()

        self.session = requests.Session()
        self.get_cookies()

    #Method to load a cookie from the file(username)
    def get_cookies(self):
        try:
            with open(self.username, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
        except:
            self.save_cookies()

    #Method to save a cookie to the file(username)
    def save_cookies(self):
        with open(self.username, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    #Get csrf token
    def get_csrf(self):
        with requests.Session() as s:
            r = s.get(self.API_URL)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
        return csrf

    #Login in Instagram
    def connect(self):
        time = int(datetime.now().timestamp())

        headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
                "referer": self.API_URL + "accounts/login/",
                "x-csrftoken": self.csrf
        }

        payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        response = self.session.post(self.API_URL + "accounts/login/ajax/", data=payload, headers=headers)
        print(response.text)
        self.save_cookies()

    def isLogedIn(self):
        text = self.session.get("https://www.instagram.com/accounts/edit/").text
        #print(text)
        soup = bs4.BeautifulSoup(text, 'lxml')
        check = soup.find("title")
        if check.text.rstrip('\n')[1:]!="Login • Instagram":
            return True
        else:
            return False

    def get_followings(self, username_id):
        if isinstance(username_id, str):
            username_id = self.get_data_by_username(username_id)['pk']

        has_next_page = True
        end_cursor = None

        followings= []

        while has_next_page:
            payload = {
                "query_hash": "d04b0a864b4b54837c0d870b0e77e076",
                "id" : username_id,
                "first": 24,
                "after": end_cursor
            }

            data = self.session.get(self.IGQ, params=payload).json()
            has_next_page = data['data']['user']['edge_follow']['page_info']['has_next_page']
            if has_next_page == True:
                end_cursor = data['data']['user']['edge_follow']['page_info']['end_cursor']

            for user in data['data']['user']['edge_follow']['edges']:
                followings.append(user['node']['username'])

        return followings

    def get_followers(self, username_id):
        if isinstance(username_id, str):
            username_id = self.get_data_by_username(username_id)['pk']

        has_next_page = True
        end_cursor = None
        followers = []

        while has_next_page:
            payload = {
                "query_hash": "c76146de99bb02f6415203be841dd25a",
                "id" : username_id,
                "first": 24,
                "after": end_cursor
            }

            data = self.session.get(self.IGQ, params=payload).json()
            print(data)
            has_next_page = data['data']['user']['edge_followed_by']['page_info']['has_next_page']
            if has_next_page == True:
                end_cursor = data['data']['user']['edge_followed_by']['page_info']['end_cursor']

            for user in data['data']['user']['edge_followed_by']['edges']:
                followers.append(user['node']['username'])
                print(user['node']['username'])

        print(followers)


    def get_data_by_username(self, username):
        link = "https://www.instagram.com/web/search/topsearch/"
        payload = {
            'query': username
        }
        data = self.session.get(link, params=payload).json()
        return data['users'][0]['user']

# if re.findall("^Login...Instagram$", text) != 1:
#     return True
# else:
#     return False
# class InstaKilo():
#
#     API_URL = "https://www.instagram.com/"
#
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.s = requests.Session()
#
#     def login(self):
#         time = int(datetime.now().timestamp())
#         csrf = self.get_csrf()
#
#         headers = {
#                 "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
#                 "x-requested-with": "XMLHttpRequest",
#                 "referer": self.API_URL + "accounts/login/",
#                 "x-csrftoken": csrf
#         }
#
#         payload = {
#             'username': self.username,
#             'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
#             'queryParams': {},
#             'optIntoOneTap': 'false'
#         }
#
#         response = self.s.post(self.API_URL + "accounts/login/ajax/", data=payload, headers=headers)
#         print(response)
#         response = json.loads(response.text)
#         print(response)
#
#     def get_csrf(self):
#         with requests.Session() as s:
#             r = s.get(self.API_URL)
#             csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
#         return csrf
#

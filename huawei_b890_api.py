import requests
import xmltodict
import hashlib


class HuaweiB890API():
    def __init__(self, user, password, ip='192.168.1.1'):
        self.user = user
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.ip = ip
        self.cookies = None

    def get_tokens(self):
        r = requests.get('http://' + self.ip + '/api/webserver/getHash')
        tokens = xmltodict.parse(r.text)
        return (tokens['response']['Param1'], tokens['response']['Param2'])

    def login(self):
        token1, token2 = self.get_tokens()
        hash_str = self.password + token1 + token2
        hash_str = hashlib.sha256(self.user.encode() + hash_str.encode())
        url_str = 'http://' + self.ip + '/api/user/login&Param1=' + token1 + \
            '&Param2=' + token2
        data_str = '<?xml version="1.0" encoding="UTF-8"?>' \
            '<request>' \
            '<Username>' + self.user + '</Username>' \
            '<Password>' + hash_str.hexdigest() + '</Password>' \
            '</request>'
        r = requests.post(
            url_str,
            data=data_str
        )
        print(r.text)
        self.cookies = r.cookies

    def diagnosis(self):
        r = requests.get('http://' + self.ip + '/api/device/diagnosis',
                         cookies=self.cookies)
        print(r.text)

    def logout(self):
        token1, token2 = self.get_tokens()
        url_str = 'http://' + self.ip + '/api/user/logout&Param1=' + token1 + \
            '&Param2=' + token2
        data_str = '<?xml version="1.0" encoding="UTF-8"?>' \
            '<request>' \
            '<Logout>1</Logout>' \
            '</request>'
        r = requests.post(
            url_str,
            data=data_str
        )
        print(r.text)

    def status(self):
        r = requests.get('http://' + self.ip + '/api/user/state-login',
                         cookies=self.cookies)
        print(r.text)

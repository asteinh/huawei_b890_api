import requests
import xmltodict
import hashlib
import time
import xml


class HuaweiB890API():
    STATUS_LOGGED_IN = 0
    STATUS_LOGGED_OUT = -1

    def __init__(self, user, password, ip='192.168.1.1', debug=False):
        self.user = user
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.ip = ip
        self.session = requests.Session()
        self.debug = debug

    def _process_response(self, r):
        if r.status_code == 200:
            try:
                text = xmltodict.parse(r.text)
            except xml.parsers.expat.ExpatError:
                # the logout call returns malformed html/xml, let's catch that
                return None, r.status_code

            if 'response' in text:
                # received response
                return text['response'], r.status_code
            else:
                # received error
                raise ValueError(text['error'])

        else:
            # non-successful status code
            return None, r.status_code

    def _get(self, endpoint):
        url = 'http://' + self.ip + endpoint
        r = self.session.get(url)

        if self.debug:
            print('GET [' + url + '] [' + str(r.status_code) + ']')

        return self._process_response(r)

    def _post(self, endpoint, data=None):
        url = 'http://' + self.ip + endpoint
        r = self.session.post(url, data=data)

        if self.debug:
            print('POST [' + url + '] [' + str(r.status_code) + ']')

        return self._process_response(r)

    def _get_tokens(self):
        r, _ = self._get('/api/webserver/getHash')
        return ((0, 0) if not r else (r['Param1'], r['Param2']))

    def _authenticate(self):
        if self.status() == self.STATUS_LOGGED_IN:
            return

        i = 3
        while self.status() != self.STATUS_LOGGED_IN and i > 0:
            self.logout()
            time.sleep(1)
            self.login()
            i -= 1

        if self.status() != self.STATUS_LOGGED_IN:
            raise ValueError('Authentication failed after multiple '
                             'attempts, aborting.')

    ###########################################################################
    # REST API calls

    def status(self):
        r, _ = self._get('/api/user/state-login')
        return (-1 if not r else int(r['State']))

    def login(self):
        if self.status() == self.STATUS_LOGGED_IN:
            return

        token1, token2 = self._get_tokens()
        ep = '/api/user/login&Param1=' + token1 + '&Param2=' + token2
        hash_str = self.password + token1 + token2
        hash_str = hashlib.sha256(self.user.encode() + hash_str.encode())
        data = '<?xml version="1.0" encoding="UTF-8"?>' \
            '<request>' \
            '<Username>' + self.user + '</Username>' \
            '<Password>' + hash_str.hexdigest() + '</Password>' \
            '</request>'
        r, c = self._post(ep, data)

    def logout(self):
        if self.status() == self.STATUS_LOGGED_OUT:
            return

        token1, token2 = self._get_tokens()
        ep = '/api/user/logout&Param1=' + token1 + '&Param2=' + token2
        data = '<?xml version="1.0" encoding="UTF-8"?>' \
            '<request>' \
            '<Logout>1</Logout>' \
            '</request>'
        r, c = self._post(ep, data=data)
        self.session = requests.Session()

    def diagnosis(self):
        self._authenticate()

        r, c = self._get('/api/device/diagnosis')
        return r

    def custom_endpoint(self, endpoint):
        self._authenticate()

        r, c = self._get(endpoint)
        return r

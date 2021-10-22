import js2py
import requests
from ehall.conf import settings
from lxml import etree


class Client:
    def __init__(self, username=None, password=None, login_url=None):
        self.username = settings.USERNAME if username is None else username
        self.password = settings.PASSWORD if password is None else password
        self.login_url = settings.LOGIN_URL if login_url is None else login_url
        self.session = requests.Session()

    def get_login_data(self):
        response = self.session.get(self.login_url)
        html = etree.HTML(response.text)
        names = html.xpath('//div/form/input[@type="hidden"]/@name')
        values = html.xpath('//div/form/input[@type="hidden"]/@value')

        salt = values.pop()
        response = self.session.get('http://authserver.njmu.edu.cn/authserver/custom/js/encrypt.js')
        password = js2py.eval_js(response.text + 'encryptAES("%s", "%s")' % (self.password, salt))

        data = dict(zip(names, values))
        data['username'] = self.username
        data['password'] = password

        return data

    def login(self, data=None):
        data = self.get_login_data() if data is None else data
        response = self.session.post(self.login_url, data=data)

        return response

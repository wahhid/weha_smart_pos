import requests


class Base()

    def __init__(self, remote_url):
        super(Base,self).__init__()
        self.remote_url = remote_url

    def authenticate(self, login, password):
        form_data 
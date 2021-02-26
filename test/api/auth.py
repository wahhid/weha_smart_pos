import requests

url = 'http://pos-dev.weha-id.com/api/auth/token'
response = requests.get(url, params = {"db": "pos-dev","login":"1901","password":"1901"})
print(response.json())
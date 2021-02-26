import requests

url = 'http://pos-dev.weha-id.com/api/pos/v1.0/product'
headers = {
    "access-token": "access_token_5b2d8694fb6ce115c42a618175c9cb1f765a44e6"
}
response = requests.post(url, data={"product_id": 2}, headers=headers)

print(response.json())
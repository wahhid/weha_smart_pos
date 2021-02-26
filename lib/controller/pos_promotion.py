from db import DBHelper
from sqlalchemy.orm import sessionmaker
from lib.model.pos_promotion import PosPromotion as PosPromotionModel
import requests

class PosPromotion(DBHelper):
    
    def __init__(self, controller):
        super(PosPromotion, self).__init__(controller) 

    def getList(self, local=True):
        if local:
            pass
        else:
            headers = {
                'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
            }
            response = requests.post(self.odoo_server_url + '/api/pos/v1.0/promotions', headers=headers)
            print(response.text)
            if response.status_code == '401':
                print("Http 401")
                return False
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return False
            else:
                promotions = response_json['data']
                return promotions


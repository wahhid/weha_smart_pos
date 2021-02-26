from db import DBHelper

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label

from lib.model.pos_category import PosCategory as PosCategoryModel

from lib.data.api_urls import ApiUrls

from datetime import datetime
import logging
import requests
import json


_logger = logging.getLogger(__name__)


class PosCategory(DBHelper):

    def __init__(self, controller):
        super(PosCategory, self).__init__(controller)
        self.model_name = 'pos.category'

    def getLocalAll(self):
        pos_categories = self.session.query(PosCategoryModel).all()
        return False, '', pos_categories

    def getAll(self):
        headers = {
            'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
        }
        response = requests.post(self.odoo_server_url + '/api/pos/v1.0/pos_categories', headers=headers)
        print(response.text)
        if response.status_code == '401':
            print("Http 401")
            return False
        
        response_json  = response.json()
        print(response_json)
        if response_json['err'] == True:
            return False, response_json['message'], []
        else:
            pos_categories = json.loads(response_json['data'])
            return True, '', pos_categories

    def getById(self, category_id, local=True):
        if local:
            self.session.query(PosCategoryModel).get(category_id)
        else:
            headers = {
                'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
            }
            form_data = {
                'category_id': category_id,
            }

            response = requests.post(self.odoo_server_url + '/api/pos/v1.0/pos_category', headers=headers, data=form_data)
            print(response.text)
            if response.status_code == '401':
                print("Http 401")
                return False
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return True, response_json['message'], {}
            else:
                pos_category = json.loads(response_json['data'])
                return False, '', pos_category

    def getLocalById(self, id):
        pos_category = self.session.query(PosCategoryModel).get(id)
        return pos_category

    def insertLocal(self, model_data):
        self.session.add(model_data)
        self.session.commit()
    
    def updateLocal(self, model_data):
        self.session.add(model_data)
        self.session.commit()

    def insert(self, model_data, local=True):
        if local:
            self.session.add(model_data)
            self.session.commit()
        else:
            pass

    def update(self, model_data, local=True):
        if local:
            self.session.add(model_data)
            self.session.commit()
        else:
            pass
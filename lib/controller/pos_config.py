from db import DBHelper

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label

from lib.model.pos_config import PosConfig as PosConfigModel
from return_handling import ReturnHandling
from lib.data.api_urls import ApiUrls

from datetime import datetime
import logging
import requests


_logger = logging.getLogger(__name__)

class PosConfig(DBHelper):

    def __init__(self, controller):
        super(PosConfig, self).__init__(controller)
        self.model_name = 'pos.config'

    def open_session_cb(self, config_id):
        form_data = {
            'config_id': config_id
        }
        headers = {
            'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
        }
        response = requests.post(self.odoo_server_url + ApiUrls.open_session_cb, headers=headers,  data=form_data)
        print(response.text)
        if response.status_code == '401':
            print("Http 401")
            return False
        
        response_json  = response.json()
        print(response_json)
        if response_json['err'] == True:
            return False
        else:
            pos_session = response_json['data'][0]
            return pos_session
    
    def open_session_local(self, config_id):
        pass

    def getById(self, config_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }

        response = requests.post('http://localhost:5000/api/category/' + str(id), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Authentication" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "Authenctication Successfully", response_json)

    def getLocalById(self, id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }

        response = requests.get('http://localhost:5000/api/v1/pos_config/' + str(id), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Authentication" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "Authenctication Successfully", response_json)

    def insertLocal(self, row):
        insert_row = PosConfigModel()
        insert_row.id = row['id']
        insert_row.name = row['name']
        insert_row.company_id = row['company_id']
        insert_row.pricelist_id = row['pricelist_id']
        self.session.add(insert_row)
        self.session.commit()

    def updateLocal(self, row):
        update_row = self.getLocalById(row['id'])
        if update_row:
            update_row.name = row['name']
            update_row.currency_id = row['currency_id']
            update_row.company_id = row['company_id']
            update_row.pricelist_id = row['pricelist_id']
            self.session.commit()
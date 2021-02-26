import requests
import json
from db import DBHelper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label
from lib.model.pos_session import PosSession as PosSessionModel
from return_handling import ReturnHandling
from datetime import datetime
import xmlrpc.client
import logging


_logger = logging.getLogger(__name__)


class PosSession(DBHelper):

    def __init__(self, controller):
        super(PosSession, self).__init__(controller)
        self.model_name = 'pos.session'
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def find_pos_session(self, company_id, config_id, user_id):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.controller.access_token
            }
            
            query = "?q=(filters:!((col:company_id,opr:eq,value:" + str(company_id) + "),(col:config_id,opr:eq,value:" + str(config_id) + "),(col:user_id,opr:eq,value:" + str(user_id) + "),(col:state,opr:eq,value:active)))"
            response = requests.get('http://localhost:5000/api/v1/pos_session/{}'.format(query), headers=headers)
            if response.status_code != 200:
                return ReturnHandling(True, "Pos Session not Found" , response.status_code)
            response_json  = response.json()
            if response_json['count'] == 0:
                #Create Pos Session
                payload = json.dumps({
                    'company_id': company_id,
                    'config': config_id,
                    'user': user_id,
                    'currency_id': 1
                })
                print(payload)
                response = requests.post('http://localhost:5000/api/v1/pos_session', headers=headers, data=payload)
                if response.status_code != 201:
                    print("Find Pos Order : Error Create")
                    return ReturnHandling(True, "Error Create" , response.json())
                response_json  = response.json()
                return ReturnHandling(False, "", response_json)
            else:
                data = {
                    "id": response_json['ids'][0],
                    "result": response_json['result'][0]
                }
                return ReturnHandling(False, "", data)
        except Exception as e:
            return ReturnHandling(True, str(e) , False)

    def find_pos_session1(self, company_id, config_id, user_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        query = "?q=(filters:!((col:company_id,opr:eq,value:" + str(company_id) + "),(col:config_id,opr:eq,value:" + str(config_id) + "),(col:user_id,opr:eq,value:" + str(user_id) + ")))"
        print(query)
        response = requests.get('http://localhost:5000/api/v1/pos_session/{}'.format(query), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query Data" , False)
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def getLocalById(self, id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }

        response = requests.post('http://localhost:5000/api/session/' + str(id), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query Data" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def create_pos_session(self, company_id, config_id, currency_id, user_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        values = {
            'company_id': company_id,
            'config_id': config_id,
            'user_id': user_id,
            'currency_id': currency_id,
        }
        response = requests.post('http://localhost:5000/api/v1/pos_session', headers=headers, data=values)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Create" , False)
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def close_pos_session(self, company_id, pos_session_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        values = {
            'company_id': company_id,
            'pos_session_id': pos_session_id,
        }
        response = requests.get('http://localhost:5000/api/v1/pos_session/closed/' + str(pos_session_id), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Create" , False)
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

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
import requests
import json
from db import DBHelper
from return_handling import ReturnHandling
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label
from lib.model.pos_payment import PosPayment as PosPaymentModel
from datetime import datetime



class PosPayment(DBHelper):

    def __init__(self, controller):
        super(PosPayment,self).__init__(controller)
        self.model_name = 'pos.payment'

    def insert(self, pos_payment):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        payload=json.dumps(pos_payment)
        response = requests.post('http://server001.weha-id.com:5000/api/v1/pos_payment', headers=headers, data=payload)
        if response.status_code != 201:
            print(response.status_code)
            return ReturnHandling(True, "Error Query" , False)
        response_json  = response.json()
        print(response_json)
        return ReturnHandling(False, "", response_json)

    
    def delete(self, pos_payment_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        response = requests.delete('http://server001.weha-id.com:5000/api/v1/pos_payment/' + str(pos_payment_id), headers=headers)
        if response.status_code != 200:
            return ReturnHandling(True, "Error Delete", False)
        response_json = response.json()
        return ReturnHandling(False, "" , response_json)
        

    def getByPosOrderId(self, pos_order_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        query = "?q=(filters:!((col:pos_order_id,opr:eq,value:" + str(pos_order_id) + ")))"
        response = requests.get('http://server001.weha-id.com:5000/api/v1/pos_payment/' + query, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query" , False)
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def getTotalByOrderId(self, pos_order_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        
        query = "?q=(filters:!((col:order_id,opr:eq,value:" + str(pos_order_id) + ")))"
        response = requests.get('http://server001.weha-id.com:5000/api/v1/pos_payment/' + query, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query" , False)   
        response_json  = response.json()
        amount_total = 0         
        for result in response_json['result']:
            amount_total = amount_total +  result['amount']
        print(f'Total Amount : {amount_total}')
        return ReturnHandling(False, "", {'amount_total': amount_total})
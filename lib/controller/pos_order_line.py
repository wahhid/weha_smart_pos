import json
import requests
from db import DBHelper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label
from sqlalchemy.exc import SQLAlchemyError
from return_handling import ReturnHandling
from lib.model.pos_order_line import PosOrderLine as PosOrderLineModel


class PosOrderLine(DBHelper):
    def __init__(self, controller):
        super(PosOrderLine,self).__init__(controller)
        self.model_name = 'pos.order.line'

    def getLocalById(self, id):
        try:
            row = self.session.query(PosOrderLineModel).get(id)
            return ReturnHandling(False, "Query Successfully", row)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return ReturnHandling(True, error, None)        

    def create_order_line(self, line):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        line.update({'company_id': 1})
        payload=json.dumps(line)
        print("CREATE ORDER LINE")
        print(payload)
        response = requests.post('http://localhost:5000/api/v1/pos_order_line', headers=headers, data=payload)
        if response.status_code != 201:
            return ReturnHandling(True, "Error Create" , response.json())
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def update_line(self, line):
        #Update Order Line
        print("Update Line")

    def localUpdate(self, line):
        try:
            self.session.add(line)
            self.session.commit()
            return ReturnHandling(False, 'Update Sucessfully', line)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return ReturnHandling(True, error, None)

    def delete_line(self, pos_order_line_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        response = requests.delete('http://localhost:5000/api/v1/pos_order_line/' + str(pos_order_line_id), headers=headers)
        if response.status_code != 200:
            return ReturnHandling(True, "Error Delete" , response.json())
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def localDelete(self, line):
        try:
            self.session.delete(line)
            self.session.commit()
            return ReturnHandling(False, 'Delete Sucessfully', None)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return ReturnHandling(True, error, None)
            
    def getTotalByOrderId(self, pos_order_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        
        query = "?q=(filters:!((col:order_id,opr:eq,value:" + str(pos_order_id) + ")))"
        response = requests.get('http://localhost:5000/api/v1/pos_order_line/' + query, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query" , False)   
        response_json  = response.json()
        amount_total = 0         
        for result in response_json['result']:
            amount_total = amount_total +  result['price_subtotal']
        print(f'Total Amount : {amount_total}')
        return ReturnHandling(False, "", {'amount_total': amount_total})

    def getByOrderId(self, pos_order_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        query = "?q=(filters:!((col:order_id,opr:eq,value:" + str(pos_order_id) + ")))"
        response = requests.get('http://localhost:5000/api/v1/pos_order_line/' + query, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query" , False)   
        response_json  = response.json()
        print(response_json)
        return ReturnHandling(False, "", response_json)



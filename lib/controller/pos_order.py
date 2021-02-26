import requests
import json
from return_handling import ReturnHandling
from db import DBHelper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label
from sqlalchemy.exc import SQLAlchemyError
from lib.model.pos_order import PosOrder as PosOrderModel
from lib.model.pos_order_line import PosOrderLine as PosOrderLineModel
from lib.model.pos_payment import PosPayment as PosPaymentModel
from lib.controller.pos_order_line import PosOrderLine as PosOrderLineController
from lib.controller.pos_payment import PosPayment as PosPaymentController
from datetime import datetime


class PosOrder(DBHelper):
      
    posorders = {
        "name": False,
        "amount_paid": 0,
        "amount_total": 0,
        "amount_tax": 0,
        "amount_return": 0,
        "pos_session_id": False,
        "pricelist_id": False,
        "partner_id": False,
        "user_id": False,
        "employee_id": False,
        "uid": False,
        "sequence_number": False,
        "creation_date": False,
        "fiscal_position_id": False,
        "server_id": False,
        "to_invoice": False,
        "lines": [],
        "statement_ids": []
    }   

    def __init__(self, controller):
        #self.odooConnector = odoorpc.ODOO('128.199.175.43', port=8069)
        super(PosOrder,self).__init__(controller)
        self.posOrderLineController = PosOrderLineController(self.controller)
        self.posPaymentController = PosPaymentController(self.controller)

    def find_pos_order(self, session_id, user_id):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.controller.access_token
            }
            
            query = "?q=(filters:!((col:pos_session_id,opr:eq,value:" + str(session_id) + "),(col:state,opr:eq,value:unpaid)))"
            response = requests.get('http://server001.weha-id.com:5000/api/v1/pos_order/{}'.format(query), headers=headers)
            if response.status_code != 200:
                return ReturnHandling(True, "Pos Order not Found" , response.status_code)
            response_json  = response.json()
            if response_json['count'] == 0:
                #Create Pos Order
                payload = json.dumps({
                    'user': user_id,
                    'pos_session': session_id
                })
                print(payload)
                response = requests.post('http://server001.weha-id.com:5000/api/v1/pos_order', headers=headers, data=payload)
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

    def create(self, pos_session_id, user_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.controller.access_token
        }

        payload = json.dumps({
            'user_id': 1,
            'pos_session_id': 1
        })

        response = requests.post('http://server001.weha-id.com:5000/api/v1/pos_order', headers=headers, data=payload)
        if response.status_code != 201:
            return ReturnHandling(True, "Error Create" , response.json())
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def getById(self, pos_order_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        response = requests.get('http://server001.weha-id.com:5000/api/v1/pos_order/' + str(pos_order_id), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Create" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    # def create_pos_order(self, pos_session):
    #     try:
    #         pos_order = PosOrderModel()
    #         pos_order.name= "Order " + datetime.now().strftime('%Y%m%d%H%M%S')
    #         pos_order.pos_session_id = pos_session
    #         pos_order.pricelist_id = 1
    #         pos_order.user_id = 2
    #         pos_order.sequence_number = 16
    #         pos_order.creation_date = datetime.now()
    #         #posorder.fiscal_position_id = False,
    #         #posorder.server_id = False,
    #         #posorder.to_invoice = False
    #         pos_order.state = "unpaid"
    #         self.session.add(pos_order)
    #         self.session.commit()
    #         return ReturnHandling(False, "Create Succesfully", pos_order)
    #     except SQLAlchemyError as e:
    #         error = str(e.__dict__['orig'])
    #         return ReturnHandling(True, error, False)

    def create_pos_order(self, pos_session_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        payload = json.dumps({
            "user_id": 3,
            "pos_session": 1
        })

        response = requests.post('http://server001.weha-id.com:5000/api/v1/pos_order', headers=headers, data=payload)
        if response.status_code != 201:
            print(response.status_code)
            return ReturnHandling(True, "Error Create" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)

    def setHold(self, pos_order_id):
        try:
            pos_order = self.session.query(PosOrderModel).get(pos_order_id)
            if not pos_order:
                return ReturnHandling(True, "Pos Order not Found", False)
            pos_order.state = 'hold'
            self.session.commit()
            return ReturnHandling(False, "Set Change to Hold", False)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return ReturnHandling(True, error, False)
        
    def setPaid(self, pos_order):
        # try:
        #     pos_order = self.session.query(PosOrderModel).get(pos_order_id)
        #     if not pos_order:
        #         return ReturnHandling(True, "Pos Order not Found", False)
        #     pos_order.amount_paid = self.posOrderLineController.getTotalByOrderId(pos_order_id)
        #     pos_order.state = 'paid'
        #     self.session.commit()
        #     return ReturnHandling(False, "Set Change to Paid", False)
        # except SQLAlchemyError as e:
        #     error = str(e.__dict__['orig'])
        #     return ReturnHandling(True, error, False)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        payload = json.dumps({
            "amount_total": pos_order['amount_total'],
            "amount_paid": pos_order['amount_paid'],
            "state": "paid"
        })

        response = requests.put('http://server001.weha-id.com:5000/api/v1/pos_order/' + str(pos_order['id']), headers=headers, data=payload)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Create" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "", response_json)
        
    def getSummary(self, pos_order_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        response = requests.get('http://server001.weha-id.com:5000/api/v1/pos_order/summary/' + str(pos_order_id), headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Query" , False)   
        response_json  = response.json()
        print(response_json)
        return ReturnHandling(False, "", response_json)

    def getJson12(self, pos_order_id):
        pos_order = self.session.query(PosOrderModel).get(pos_order_id)
        pos_order_lines = self.session.query(PosOrderLineModel).filter_by(order_id=pos_order_id).all()
        for pos_order_line in pos_order_lines:
            lines.append(
                [
                    0,
                    0,
                    {
                        "qty": pos_order_line.qty,
                        "price_unit": pos_order_line.price_unit,
                        "price_subtotal": pos_order_line.price_subtotal,
                        "price_subtotal_incl": pos_order_line.price_subtotal_incl,
                        "discount": 0,
                        "product_id": pos_order_line.product_id,
                        "tax_ids": [
                        [
                            6,
                            False,
                            []
                        ]
                        ],
                        "id": pos_order_line.id,
                        "pack_lot_ids": [],

                    }
                ]
            )

        journals = self.journalController.getLocalByPosOrderId(pos_order_id=pos_order_id, local=True)
        for journal in journals:
            statement_id = [
                0,
                0,
                {
                    "name": "2020-07-08 13:55:51",
                    "statement_id": pos_payment.payment_method_id,
                    "amount": pos_payment.amount,
                    "account_id": "",
                    "journal_id": ""
                }
            ]
            statement_ids.append(statement_id)
        
        data = { 
            "data" : {
                "name": pos_order.name,
                "amount_paid": pos_order.amount_paid,
                "amount_total": pos_order.amount_paid,
                "amount_tax": 0,
                "amount_return": 0,
                "lines": lines,
                "statement_ids": statement_ids,
                "pos_session_id": pos_order.pos_session_id,
                "pricelist_id": 1,
                "partner_id": False,
                "user_id": self.uid,
                "employee_id": False,
                "uid": "00001-083-0016",
                "sequence_number": 16,
                "creation_date": "2020-07-08T13:55:51.929Z",
                "fiscal_position_id": False,
                "server_id": False,
                "to_invoice": False
            }
        }
        pos_order_json.append(data)

    def getJson(self, pos_order_id):
        pos_order_json = []
        lines = []
        statement_ids = []
        session_info = []

        pos_order = self.session.query(PosOrderModel).get(pos_order_id)
        
        pos_order_lines = self.session.query(PosOrderLineModel).filter_by(order_id=pos_order_id).all()
        for pos_order_line in pos_order_lines:
            lines.append(
                [
                    0,
                    0,
                    {
                        "qty": pos_order_line.qty,
                        "price_unit": pos_order_line.price_unit,
                        "price_subtotal": pos_order_line.price_subtotal,
                        "price_subtotal_incl": pos_order_line.price_subtotal_incl,
                        "discount": 0,
                        "product_id": pos_order_line.product_id,
                        "tax_ids": [
                        [
                            6,
                            False,
                            []
                        ]
                        ],
                        "id": pos_order_line.id,
                        "pack_lot_ids": []
                    }
                ]
            )
        
        pos_payments = self.posPaymentController.getByPosOrderId(pos_order_id=pos_order_id, local=True)
        for pos_payment in pos_payments:
            statement_id = [
                0,
                0,
                {
                    "name": "2020-07-08 13:55:51",
                    "payment_method_id": pos_payment.payment_method_id,
                    "amount": pos_payment.amount,
                    "payment_status": "",
                    "ticket": "",
                    "card_type": "",
                    "transaction_id": ""
                }
            ]
            statement_ids.append(statement_id)

        data = { 
            "data" : {
                "name": pos_order.name,
                "amount_paid": pos_order.amount_paid,
                "amount_total": pos_order.amount_paid,
                "amount_tax": 0,
                "amount_return": 0,
                "lines": lines,
                "statement_ids": statement_ids,
                "pos_session_id": pos_order.pos_session_id,
                "pricelist_id": 1,
                "partner_id": False,
                "user_id": self.uid,
                "employee_id": False,
                "uid": "00001-083-0016",
                "sequence_number": 16,
                "creation_date": "2020-07-08T13:55:51.929Z",
                "fiscal_position_id": False,
                "server_id": False,
                "to_invoice": False
            }
        }
        pos_order_json.append(data)
        
        self.models.execute_kw(self.db_name, self.uid, self.password,'pos.order', 'create_from_ui',[pos_order_json], {})
        pos_order.state = 'sync'
        self.session.commit()
        
        return pos_order_json

    def toJson(self):
        pass


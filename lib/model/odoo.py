import xmlrpc.client
import datetime
import json
import requests


class Odoo():

    def __init__(self):
        """
            create invoice
            create invoice line
        """
        self.DATA = "pos-dev" # db name
        self.USER = "admin" # email address
        self.PASS = "P@ssw0rd" # password
        self.PORT = "8069" # port
        self.URL  = "http://128.199.175.43" # base url
        self.URL_COMMON = "{}:{}/xmlrpc/2/common".format(
            self.URL, self.PORT)
        self.URL_OBJECT = "{}:{}/xmlrpc/2/object".format(
            self.URL, self.PORT)

    def initPosOrder(self, session_id):
        pass        
 
    def authenticateOdoo(self):
        print("odoo authenticate")
        self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON)
        print(self.ODOO_COMMON.version())
        self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT)
        self.UID = self.ODOO_COMMON.authenticate(
            self.DATA
            , self.USER
            , self.PASS
            , {})
        print(self.UID)

    def posOrderAdd(self, pos_order):
        print(self.UID)
        print(pos_order)
        invoice_id = self.ODOO_OBJECT.execute_kw(
            self.DATA
            , self.UID
            , self.PASS
            , 'pos.order'
            , 'create_from_ui'
            , [pos_order]
            , {},
            )
        if invoice_id:
            return invoice_id
        else:
            return None

    def getOpenPosSession(self, config_id):
        try:
            pos_session_id = self.ODOO_OBJECT.execute_kw(
                self.DATA
                ,self.UID
                ,self.PASS
                ,'pos.session'
                ,'search'
                ,[[['config_id','=', config_id],['state','=','opened']]] 
            )
            if pos_session_id:
                return pos_session_id
            else:
                return self.createPosSession(config_id)
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    def createPosSession(self, config_id):
        try:
            pos_config_id = self.ODOO_OBJECT.execute_kw(
                self.DATA
                ,self.UID
                ,self.PASS
                ,'pos.session'
                ,'create'
                ,[{
                    'user_id': self.UID,
                    'config_id': config_id
                }]   
            )
            return pos_config_id
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    def getProductByBarcode(self, barcode):
        product_ids = self.ODOO_OBJECT.execute_kw(
            self.DATA
            ,self.UID
            ,self.PASS
            ,'product.product'
            ,'search'
            ,[[['barcode','=',barcode],['available_in_pos','=', True]]]
            )
        if product_ids:
            record = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS,'product.product', 'read', [product_ids], {'fields': ['display_name', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id',
                 'barcode', 'default_code', 'to_weight', 'uom_id', 'description_sale', 'description',
                 'product_tmpl_id','tracking']})
            return record[0]
        else:
            return None

def main():
    ''' url_login ='https://api.testing.pethersolutions.com/ghi/c/ws/ws-login.php'
    urlSub = 'https://api.testing.pethersolutions.com/ghi/reg/ws/'
    payload = {'op':'login' 
            , 'user':'christian'
            , 'pass' : 'christian123'
            , 'orgid' : '1'
            , 'mid' : 'undefined' 
            , 'midtype' : 'host' 
            , 'remHost' : '154.72.167.161' 
            , 'magik' : '1534110443' 
            }
    r = requests.post(url_login, data=payload)
    data = r.json() '''
    pos_orders = [
        {"data" : {
        "name": "Order 54353543543",
        "amount_paid": 29,
        "amount_total": 29,
        "amount_tax": 0,
        "amount_return": 1,
        "lines": [
            [
            0,
            0,
            {
                "qty": 1,
                "price_unit": 12.5,
                "price_subtotal": 12.5,
                "price_subtotal_incl": 12.5,
                "discount": 0,
                "product_id": 25,
                "tax_ids": [
                [
                    6,
                    False,
                    []
                ]
                ],
                "id": 1,
                "pack_lot_ids": []
            }
            ],
            [
            0,
            0,
            {
                "qty": 1,
                "price_unit": 16.5,
                "price_subtotal": 16.5,
                "price_subtotal_incl": 16.5,
                "discount": 0,
                "product_id": 23,
                "tax_ids": [
                [
                    6,
                    False,
                    []
                ]
                ],
                "id": 2,
                "pack_lot_ids": []
            }
            ]
        ],
        "statement_ids": [
            [
            0,
            0,
            {
                "name": "2020-07-08 13:55:51",
                "payment_method_id": 1,
                "amount": 30,
                "payment_status": "",
                "ticket": "",
                "card_type": "",
                "transaction_id": ""
            }
            ]
        ],
        "pos_session_id": 1,
        "pricelist_id": 1,
        "partner_id": False,
        "user_id": 2,
        "employee_id": False,
        "uid": "00001-083-0016",
        "sequence_number": 16,
        "creation_date": "2020-07-08T13:55:51.929Z",
        "fiscal_position_id": False,
        "server_id": False,
        "to_invoice": False
        }
        }
    ]

    od = Odoo()
    od.authenticateOdoo()
    #od.posOrderAdd(pos_orders)
    product_id = od.getProductByBarcode('1231231231')    
    print(product_id)
    pos_config_id = od.createPosSession(1)
    print(pos_config_id)
    

if __name__ == '__main__':
    main()

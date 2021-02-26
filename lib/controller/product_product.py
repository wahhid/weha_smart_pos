import requests
from db import DBHelper
from sqlalchemy.orm import sessionmaker
from lib.model.product_product import ProductProduct as ProductProductModel
from return_handling import ReturnHandling

class ProductProduct(DBHelper):
    
    def __init__(self, controller):
        super(ProductProduct, self).__init__(controller)
        self.model_name = 'product.product'
        self.productProductModel = ProductProductModel()

    def getProducts(self):
        headers = {
            'access-token': self.controller.access_token
        }
        return self.api_post(endpoint='/api/v1/pos/products', headers=headers)
    
    def getLocalProducts(self):
        headers = {
        }
        response = requests.post(self.odoo_server_url + '/api/smartpos/products', headers=headers)
        print(response.text)
        if response.status_code == '401':
            print("Http 401")
            return False
        
        response_json  = response.json()
        print(response_json)
        if response_json['err'] == True:
            return False, response_json['message'], []
        else:
            account_journals = json.loads(response_json['data'])
            return True, '', account_journals

    def getLocalById(self, product_id):
        product_product = self.session.query(ProductProductModel).get(product_id)
        return product_product
        
    def getById(self, product_id):
        form_data = {
            'product_id': product_id,
        }

        headers = {
        'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
        }

        response = requests.get('/api/v1/product/barcode/')
        return response
        
    def getLocalByBarcode(self, barcode):
        #product = self.session.query(ProductProductModel).filter_by(barcode=barcode).first()
        #return  product
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }

        response = requests.post('http://localhost:5000/api/smartpos/v1.0/products/1', headers=headers)
        print(response.text)
        if response.status_code != '200':
            print("Http 401")
            return 
    
        response_json  = response.json()
        print(response_json)
        if response_json['err'] == True:
            return False, response_json['message'], []
        else:
            account_journals = json.loads(response_json['data'])
            return True, '', account_journals
        
    def getByBarcode(self, barcode):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        query = "?q=(filters:!((col:barcode,opr:eq,value:" + barcode + ")))"
        response = requests.get('http://localhost:5000/api/v1/product/{}'.format(query), headers=headers)
        print(type(response.status_code))
        if response.status_code != 200:
            print("Response not 200")
            return ReturnHandling(True, "Error Response", False)
        response_json  = response.json()
        print(response_json)
        return ReturnHandling(False, '', response_json)

    def getLocalProductById(self, id):
        product = self.session.query(ProductProductModel).get(id)
        return product

    def getLocalProductByBarcode(self, barcode):
        product = self.session.query(ProductProductModel).filter_by(barcode=barcode).first() 
        return product

    def insertLocal(self, product_product):
        self.session.add(product_product)
        self.session.commit()
    
    def updateLocal(self, product_product):
        self.session.add(product_product)
        self.session.commit()

    def insert(self, product_product):
        strSQL = """
            INSERT INTO product_product 
                (
                    id,display_name,lst_price,standard_price,categ_id,pos_categ_id,taxes_id,
                    barcode,default_code,to_weight,uom_id,description_sale,description,
                    product_tmpl_id,tracking
                )
            VALUES(
                {},'{}',{},{},{},{},{},
                '{}','{}','{}',{},'{}','{}',
                {},'{}'
            )
        """.format( 
            product_product['id'], product_product['display_name'], product_product['lst_price'], product_product['standard_price'], product_product['categ_id'] and product_product['categ_id'][0] or 'Null', product_product['pos_categ_id'] and product_product['pos_categ_id'][0] or 'Null', 0, 
            product_product['barcode'], product_product['default_code'], product_product['to_weight'], product_product['uom_id'][0] or 'NULL', product_product['description_sale'], product_product['description'], 
            product_product['product_tmpl_id'][0] or 'NULL', product_product['tracking']

        )
        print(strSQL)
        cur = self.conn.cursor()
        cur.execute(strSQL)
        self.conn.commit()
        
    def update(self, product_product):
        pass
        #product = ProductProductModel.get(product_product['id'])
        #if product:
        #    product.display_name = product_product['display_name']
            
        
        # strSQL = """
        #     UPDATE product_product 
        #         SET display_name='{}', lst_price={}, standard_price={}, categ_id={}, pos_categ_id={}, taxes_id={},
        #             barcode='{}', default_code='{}', to_weight='{}', uom_id={}, description_sale='{}', description='{}',
        #             product_tmpl_id={}, tracking='{}'
        #     WHERE id={}
            
        # """.format( 
        #     product_product['display_name'], product_product['lst_price'], product_product['standard_price'], product_product['categ_id'] and product_product['categ_id'][0] or 'Null', product_product['pos_categ_id'] and product_product['pos_categ_id'][0] or 'Null', 0, 
        #     product_product['barcode'], product_product['default_code'], product_product['to_weight'], product_product['uom_id'][0] or 'NULL', product_product['description_sale'], product_product['description'], 
        #     product_product['product_tmpl_id'][0] or 'NULL', product_product['tracking'],
        #     product_product['id']

        # )
        # print(strSQL)
        # cur = self.conn.cursor()
        # cur.execute(strSQL)
        # self.conn.commit()
        
from db import DBHelper
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from sqlalchemy_paginator import Paginator

from lib.model.res_partner import ResPartner as ResPartnerModel

import requests

class ResPartner(DBHelper):
    
    def __init__(self, controller):
        super(ResPartner, self).__init__(controller) 
        self.model_name = 'res.partner'

    def getLocalAll(self):
        res_partners = self.session.query(ResPartnerModel).all()
        return res_partners

    def getTotalCount(self):
        return self.session.query(func.count(ResPartnerModel.id)).scalar() 
        #return self.session.query(ResPartnerModel).count()

    def page(self, row_number, page_number):
        totalCount = self.getTotalCount()
        print("Total Count", totalCount)
        totalPage = int(totalCount / row_number)
        print("Total Page", totalPage)
        query = self.session.query(ResPartnerModel)
        paginator = Paginator(query, row_number)
        pagination = paginator.page(page_number)
        print("page number of current page in iterator", pagination.number)
        print("this is a list that contains the records of current page", pagination.object_list)
        return pagination

    def getLocalFilterByName(self, name):
        res_partners = self.session.query(ResPartnerModel).filter(ResPartnerModel.name.like(name + "%")).all()
        return res_partners

    def getPartners(self, local=True):
        if local:
            pass
        else:
            headers = {
                'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
            }
            response = requests.post(self.odoo_server_url + '/api/pos/v1.0/partners', headers=headers)
            print(response.text)
            if response.status_code == '401':
                print("Http 401")
                return False
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return False
            else:
                partners = response_json['data']
                return partners


    def getLocalById(self, id):
        res_partner = self.session.query(ResPartnerModel).get(id)
        return res_partner

    def insertLocal(self, model_data):
        self.session.add(model_data)
        self.session.commit()
    
    def updateLocal(self, model_data):
        self.session.add(model_data)
        self.session.commit()

    def getPartnerById(self, id):
        partner = self.models.execute_kw(self.db_name, self.uid, self.password, self.model_name, 'read', [id], {'fields': self.fields})
        return partner and partner[0] or False

    def getLocalPartnerById(self,id):
        res_partner = self.session.query(ResPartnerModel).get(id)
        return res_partner or False

    def getPartner(self, barcode):
        res_partner_id = self.models.execute_kw(self.db_name, self.uid, self.password,  self.model_name, 'search', [[['barcode','=', barcode]]], {'limit': 1})
        if not res_partner_id:
            return False
        res_partner = self.models.execute_kw('pos-dev', self.uid, self.password, self.model_name, 'read', [res_partner_id], {'fields': self.fields})
        return res_partner

    def insertLocalPartner(self, res_partner):
        pass

    def updateLocalPartner(self, res_partner):
        
        pass

    def insertPartner(self, product_product):
        strSQL = """
            INSERT INTO res_partner 
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
        
    def updatePartner(self, product_product):
        strSQL = """
            UPDATE product_product 
                SET display_name='{}', lst_price={}, standard_price={}, categ_id={}, pos_categ_id={}, taxes_id={},
                    barcode='{}', default_code='{}', to_weight='{}', uom_id={}, description_sale='{}', description='{}',
                    product_tmpl_id={}, tracking='{}'
            WHERE id={}
            
        """.format( 
            product_product['display_name'], product_product['lst_price'], product_product['standard_price'], product_product['categ_id'] and product_product['categ_id'][0] or 'Null', product_product['pos_categ_id'] and product_product['pos_categ_id'][0] or 'Null', 0, 
            product_product['barcode'], product_product['default_code'], product_product['to_weight'], product_product['uom_id'][0] or 'NULL', product_product['description_sale'], product_product['description'], 
            product_product['product_tmpl_id'][0] or 'NULL', product_product['tracking'],
            product_product['id']

        )
        print(strSQL)
        cur = self.conn.cursor()
        cur.execute(strSQL)
        self.conn.commit()
        

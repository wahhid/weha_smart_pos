import couchdb
import json
import odoorpc
import xmlrpc.client
import sqlite3
from sqlite3 import Error
import sqlalchemy as db
from db import DBHelper

class PosLogin(DBHelper):

    def __init__(self):
        super(PosLogin, self).__init__()
        #self.odooConnector = odoorpc.ODOO('128.199.175.43', port=8069)

        self.conn = sqlite3.connect('../../pos.sqlite')
        #self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format('http://128.199.175.43:8069'))
        #self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format('http://128.199.175.43:8069'))

    def getUserInfo(self):
        user = self.models.execute_kw('pos-dev', self.uid, self.password,'res.users', 'read', [self.uid], {'fields': ['name', 'email']})
        print(user[0])
        return user[0]

    def connect_db(self):
        self.couch = couchdb.Server('http://admin:admin123@128.199.175.43:5984/')
        self.paid_db = self.couch['paid_posorders']
        self.unpaid_db = self.couch['unpaid_posorders']

    def getJson(self):
        return json.dumps(self.posorder)
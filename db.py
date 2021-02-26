import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker
import xmlrpc.client
from dotenv import load_dotenv
import os
import requests
import json
from return_handling import ReturnHandling

Base = declarative_base()

class DBHelper():
    
    def __init__(self, controller):
        self.controller = controller
        load_dotenv(verbose=True)

        #SQLAlchemy
        self.sqlite_dbname = str(os.getenv("SQLITE_DB_FILE"))
        self.engine = db.create_engine('sqlite:///' + self.sqlite_dbname)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        #Odoo
        self.db_name = os.getenv("ODOO_DB_NAME")
        self.odoo_server_url = os.getenv("ODOO_SERVER_URL")
        self.odoo_server_ip = os.getenv("ODOO_SERVER_IP")
        self.odoo_server_port= os.getenv("ODOO_SERVER_PORT")
        self.odoo_access_token = os.getenv("ODOO_ACCESS_TOKEN")
        self.url = self.odoo_server_url + ":" + self.odoo_server_port

    def login(self, username, password):        
        self.username = username
        self.password = password
        self.uid = self.common.authenticate(self.db_name, username, password, {})
        return self.uid

    def db_login(self, username, password):
        pass

    def auth(self):
        response = requests.get('http://pos-dev.server007.weha-id.com/api/auth/token?db='+ self.db_name + '&login=' + self.login + '&password=' + self.password)
        print(response.status_code)
        if str(response.status_code) != '200':
            print("Http 401")
            return True, "Error Authentication" , False
        
        response_json = response.json()
        print(response_json)
        return False, "Authenctication Successfully", response_json

    def api_get(self, endpoint, headers={}, form_data={}):
        err, message, auth = self.auth()
        if not err:
            headers.update({'access-token': auth['access_token']})
            response = requests.get(self.odoo_server_url + endpoint, headers=headers, data=form_data)
            print(response.text)
            if str(response.status_code) != '200':
                print("Http 401")
                return False, "Error", []
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return True, response_json['message'], []
            else:
                datas = response_json['data']
                return False, '', datas
        else:
            return err, message, []

    def api_post(self, endpoint, headers={}, form_data={}):
        response = requests.post(self.odoo_server_url + endpoint, headers=headers, data=form_data)
        
        if str(response.status_code) != '200':
            print("Http 401")
            return ReturnHandling(False, "Error HTTP", [])
            
        response_json  = response.json()
        print("API POST")
        print(response_json)
        return ReturnHandling(response_json['err'], response_json['message'], response_json['data'])

    def api_put(self, endpoint, headers={}, form_data={}):
        pass 

    def api_delete(self, endpoint, headers={}, form_data={}):
        pass 

    def odoo_get(self, endpoint, headers={}, form_data={}):
        err, message, auth = self.auth()
        if not err:
            headers.update({'access-token': auth['access_token']})
            response = requests.get(self.odoo_server_url + endpoint, headers=headers, data=form_data)
            print(response.text)
            if str(response.status_code) != '200':
                print("Http 401")
                return False, "Error", []
            
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                return True, response_json['message'], []
            else:
                datas = response_json['data']
                return False, '', datas
        else:
            return err, message, []

    def odoo_post(self, endpoint, headers={}, form_data={}):
        response = requests.post(self.odoo_server_url + endpoint, headers=headers, data=form_data)
        
        if str(response.status_code) != '200':
            print("Http 401")
            return ReturnHandling(False, "Error HTTP", [])
            
        response_json  = response.json()
        print("API POST")
        print(response_json)
        return ReturnHandling(response_json['err'], response_json['message'], response_json['data'])

    def odoo_put(self, endpoint, headers={}, form_data={}):
        pass 
    
    def odoo_delete(self, endpoint, headers={}, form_data={}):
        pass 

    def get(self, id):
        pass 

    def create(self, values):
        pass

    def write(self, id, values):
        pass 

    def unlink(self, id):
        pass
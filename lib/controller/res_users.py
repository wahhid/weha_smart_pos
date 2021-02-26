from db import DBHelper

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label

from sqlalchemy_paginator import Paginator

from lib.model.res_users import ResUsers as ResUsersModel
from return_handling import ReturnHandling
from lib.data.api_urls import ApiUrls

from datetime import datetime
import logging
import requests
import json


_logger = logging.getLogger(__name__)


class ResUsers(DBHelper):

    def __init__(self, controller):
        super(ResUsers, self).__init__(controller)
        self.model_name = 'res.users'
        self.resUsersModel = ResUsersModel()

    def getLocalById(self, res_user_id):
        self.session.query(ResUsersModel).get(res_user_id)

    def getById(self, res_user_id):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }
        form_data = {
            'user_id': res_user_id
        }
        return self.api_post('/api/pos/v1.0/user', headers=headers, form_data=form_data)

    def getByName(self, name):
        headers = {
            'Authorization': 'Bearer ' + self.controller.access_token
        }

        response = requests.post('http://localhost:5000/api/user/name/' + name, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            return ReturnHandling(True, "Error Authentication" , False)
            
        response_json  = response.json()
        return ReturnHandling(False, "Authenctication Successfully", response_json)


    def login(self, email, password):
        pass 

    def api_login(self, db, login, password):
        # response = requests.get('http://pos-dev.server007.weha-id.com/api/auth/token?db='+ db + '&login=' + login + '&password=' + password)
        # print(response.status_code)
        # if str(response.status_code) != '200':
        #     print("Http 401")
        #     return ReturnHandling(True, "Error Authentication" , False)
        
        # response_json  = response.json()
        # #print(response_json)
        # return ReturnHandling(False, "Authenctication Successfully", response_json)
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                'username': login, 
                'password': password,
                'provider': 'db',
                'refresh': True
            }

            data=json.dumps(payload)
            response = requests.post('http://localhost:5000/api/v1/security/login', headers=headers, data=data)
            if response.status_code != 200:
                print(response.status_code)
                return ReturnHandling(True, "Error Authentication" , False)
            response_json  = response.json()
            return ReturnHandling(False, "Authenctication Successfully", response_json)
        except requests.exceptions.ConnectionError as err:
            return ReturnHandling(True, "Error Server Connection", [])

    def page(self):
        query = self.session.query(ResUsersModel)
        paginator = Paginator(query, 5)
        for page in paginator:
            print("page number of current page in iterator", page.number)
            print("this is a list that contains the records of current page", page.object_list)
from db import DBHelper

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import label

from lib.model.account_journal import AccountJournal as AccountJournalModel

from lib.data.api_urls import ApiUrls

from datetime import datetime
import logging
import requests
import json


_logger = logging.getLogger(__name__)


class AccountJournal(DBHelper):

    def __init__(self):
        super(AccountJournal, self).__init__()
        self.model_name = 'account.journal'

    def getLocalAll(self):
        account_journals = self.session.query(AccountJournalModel).all()
        return False, '', account_journals

    def getAll(self):
        headers = {
            'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
        }
        response = requests.post(self.odoo_server_url + '/api/pos/v1.0/journals', headers=headers)
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

    def getById(self, journal_id):

        headers = {
            'access-token': 'access_token_03156b5e6bf304f52d57d9916e156b33ca4ec14d'
        }
        form_data = {
            'journal_id': journal_id,
        }

        response = requests.post(self.odoo_server_url + '/api/pos/v1.0/journal', headers=headers, data=form_data)
        print(response.text)
        if response.status_code == '401':
            print("Http 401")
            return False
        
        response_json  = response.json()
        print(response_json)
        if response_json['err'] == True:
            return True, response_json['message'], {}
        else:
            journal = json.loads(response_json['data'])
            return False, '', journal_id

    def getLocalById(self, id):
        journal = self.session.query(AccountJournalModel).get(id)
        return journal

    def insertLocal(self, model_data):
        self.session.add(model_data)
        self.session.commit()
    
    def updateLocal(self, model_data):
        self.session.add(model_data)
        self.session.commit()

    def insert(self, model_data, local=True):
        if local:
            self.session.add(model_data)
            self.session.commit()
        else:
            pass

    def update(self, model_data, local=True):
        if local:
            self.session.add(model_data)
            self.session.commit()
        else:
            pass
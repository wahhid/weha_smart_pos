
from lib.sync.sync_helper import SyncHelper
from lib.model.pos_config import PosConfig as PosConfigModel
from lib.controller.pos_config import PosConfig as PosConfigController
from datetime import datetime
from pytz import timezone
import pytz
from dotenv import load_dotenv
import os


class PosConfig(SyncHelper):
    
    def __init__(self, controller):
        super(PosConfig, self).__init__(controller)
        self.model_name = 'pos.config'
        load_dotenv(verbose=True)
        self.config_id = os.getenv("CONFIG_ID")
        self.posConfigModel = PosConfigModel()
        self.posConfigController = PosConfigController(self.controller)


    def sync(self):
        print("Sync Pos Config")
        print(self.model_name)
        sync_process = self.getSyncProcessbyModelName(self.model_name)
        if sync_process:
            print(sync_process.last_sync)
            #last_sync = datetime.strptime(sync_process.last_sync, ('%Y-%m-%d %H:%M:%S')).astimezone(pytz.utc)
            
            #last_sync = sync_process.last_sync.strftime()
            domain = [['id','=', self.config_id],['write_date','>', sync_process.last_sync.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')]]
            print(domain)
            fields = self.fields.pos_config
            ids = self.models.execute_kw(self.db_name, self.uid, self.password, self.model_name, 'search', [domain])
            print(ids)
            for id in ids:
                rows = self.models.execute_kw(self.db_name, self.uid, self.password, self.model_name, 'read', [id], {'fields': fields})
                print(rows)
                row = rows[0]
                data = {
                    'id': row['id'],
                    'name': row['name'],
                    'currency_id' : row['currency_id'][0],
                    'company_id': row['company_id'][0],
                    'pricelist_id': row['pricelist_id'][0],
                }
                if self.posConfigController.getLocalById(row['id']):
                    self.posConfigController.updateLocal(data)
                else:
                    self.posConfigController.insertLocal(data)

            self.updateSyncProcessTimeModel(self.model_name)
        


from db import DBHelper
from sqlalchemy.orm import sessionmaker
from lib.model.sync_process import SyncProcess as SyncProcessModel
from lib.data.server_fields import ServerFields
from datetime import datetime




class SyncHelper(DBHelper):

    def __init__(self, controller):
        super(SyncHelper, self).__init__(controller)
        self.fields = ServerFields()
        self.syncProcessModel = SyncProcessModel()

    def getSyncProcessbyModelName(self, model_name):
        print("Sync Process By Model Name")
        print(model_name)
        sync_process = self.session.query(SyncProcessModel).filter_by(model_name=model_name).first()
        print(sync_process)
        return sync_process
        
    def updateSyncProcessTimeModel(self, model_name):
        print("Update Sync Process Time")
        sync_process = self.session.query(SyncProcessModel).filter_by(model_name=model_name).first()
        sync_process.last_sync = datetime.now()
        self.session.commit()

        
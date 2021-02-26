from lib.sync.sync_helper import SyncHelper
from lib.model.pos_category import PosCategory as PosCategoryModel
from lib.controller.pos_category import PosCategory as PosCategoryController
from datetime import datetime
from pytz import timezone
import pytz

class PosCategory(SyncHelper):
    
    def __init__(self,controller):
        super(PosCategory, self).__init__(controller)
        self.model_name = 'pos.category'
        self.posCategoryModel = PosCategoryModel()
        self.posCategoryController = PosCategoryController(self.controller)
        
    def sync(self):
        print("Sync Pos Category")
        sync_process = self.getSyncProcessbyModelName(self.model_name)
        if sync_process:
            print(sync_process.last_sync)
            syncdate = sync_process.last_sync.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
            form_data = {
                'syncdate': syncdate
            }
            err, message, datas = self.api_post('/api/pos/v1.0/pos_category_sync', form_data=form_data)
            if not err:
                for pos_category_dict in datas:
                    print("Pos Category")
                    print(pos_category_dict)
                    pos_category = self.posCategoryController.getLocalById(pos_category_dict['id'])
                    if pos_category is not None:
                        for key in pos_category_dict:
                            print(pos_category[key])
                            setattr(pos_category, key, pos_category_dict[key])   
                        self.posCategoryController.updateLocal(product)
                    else:
                        pos_category = PosCategoryModel()
                        for key in pos_category_dict:
                            print(pos_category_dict[key])
                            setattr(pos_category, key, pos_category_dict[key])                                   
                        self.posCategoryController.insertLocal(pos_category)
                        
                self.updateSyncProcessTimeModel(self.model_name)


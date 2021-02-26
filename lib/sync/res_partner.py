from lib.controller.res_partner import ResPartner as ResPartnerController
from lib.model.res_partner import ResPartner as ResPartnerModel
from lib.sync.sync_helper import SyncHelper
from datetime import datetime
from pytz import timezone
import pytz

class ResPartner(SyncHelper):
    
    def __init__(self, controller):
        super(ResPartner, self).__init__(controller)
        self.model_name = 'res.partner'
        self.resPartnerModel = ResPartnerModel()
        self.resPartnerController = ResPartnerController(self.controller)

    def sync(self):
        print("Sync Res Partner")
        sync_process = self.getSyncProcessbyModelName(self.model_name)
        if sync_process:
            print(sync_process.last_sync)
            syncdate = sync_process.last_sync.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
            form_data = {
                'syncdate': syncdate
            }
            err, message, datas = self.api_post('/api/pos/v1.0/res_partner_sync', form_data=form_data)
            if not err:
                for res_partner_dict in datas:
                    print("Res Partner")
                    print(res_partner_dict)
                    res_partner = self.resPartnerController.getLocalById(res_partner_dict['id'])
                    if res_partner is not None:
                        for key in res_partner_dict:
                            print(res_partner_dict[key])
                            setattr(res_partner, key, res_partner_dict[key])   
                        self.resPartnerController.updateLocal(res_partner)
                    else:
                        res_partner = ResPartnerModel()
                        for key in res_partner_dict:
                            print(res_partner_dict[key])
                            setattr(res_partner, key, res_partner_dict[key])   
                        self.resPartnerController.insertLocal(res_partner)
                        
                self.updateSyncProcessTimeModel(self.model_name)
        


from lib.sync.sync_helper import SyncHelper
from lib.model.account_journal import AccountJournal as AccountJournalModel
from lib.controller.account_journal import AccountJournal as AccountJournalController
from datetime import datetime
from pytz import timezone
import pytz

class AccountJournal(SyncHelper):
    
    def __init__(self):
        super(AccountJournal, self).__init__()
        self.model_name = 'account.journal'
        self.accountJournalModel = AccountJournalModel()
        self.accountJournalController = AccountJournalController()

    def sync(self):
        print("Sync Account Journal")
        sync_process = self.getSyncProcessbyModelName(self.model_name)
        if sync_process:
            print(sync_process.last_sync)
            syncdate = sync_process.last_sync.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
            form_data = {
                'syncdate': syncdate
            }
            err, message, datas = self.api_post('/api/pos/v1.0/account_journal_sync', form_data=form_data)
            if not err:
                for account_journal_dict in datas:
                    print("Account Journal")
                    print(account_journal_dict)
                    account_journal = self.accountJournalController.getLocalById(account_journal_dict['id'])
                    if account_journal is not None:
                        for key in account_journal_dict:
                            print(account_journal[key])
                            setattr(account_journal, key, account_journal_dict[key])   
                        self.accountJournalController.updateLocal(account_journal)
                    else:
                        account_journal = AccountJournalModel()
                        for key in account_journal_dict:
                            print(account_journal_dict[key])
                            setattr(account_journal, key, account_journal_dict[key])                                   
                        self.accountJournalController.insertLocal(account_journal)
                        
                self.updateSyncProcessTimeModel(self.model_name)


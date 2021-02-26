# #View
# from lib.view.pos_login import PosLoginUi
# from lib.view.pos_payment import PosPaymentUi
# from lib.view.pos_customer import PosCustomerUi
# from lib.view.pos_promotion import PosPromotionUi

# #Model
# from lib.model.pos_login import PosLoginModel
from lib.model.res_users import ResUsers as ResUsersModel
from lib.model.product_product import ProductProduct as ProductProductModel
from lib.model.pos_config import PosConfig as PosConfigModel
from lib.model.pos_category import PosCategory as PosCategoryModel

# #Sync
from lib.sync.product_product import ProductProduct as ProductProductSync
from lib.sync.pos_config import PosConfig as PosConfigSync
from lib.sync.pos_category import PosCategory as PosCategorySync
from lib.sync.res_partner import ResPartner as ResPartnerSync
from lib.sync.account_journal import AccountJournal as AccountJournalSync


# #Controller
from lib.controller.product_product import ProductProduct as ProductProductController
from lib.controller.pos_order import PosOrder as PosOrderController
from lib.controller.pos_order_line import PosOrderLine as PosOrderLineController
from lib.controller.pos_payment import PosPayment as PosPaymentController
from lib.controller.pos_config import PosConfig as PosConfigController
from lib.controller.pos_session import PosSession as PosSessionController
from lib.controller.pos_category import PosCategory as PosCategoryController
from lib.controller.res_users import ResUsers as ResUserController


# #Receipt
from lib.printer.receipt01 import Receipt01
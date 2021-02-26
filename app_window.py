from PyQt5 import QtWidgets, QtCore, uic

# View
#from lib.view.pos_customer import PosCustomerUi
#from lib.view.pos_promotion import PosPromotionUi

# Controller
from lib.controller.product_product import ProductProduct as ProductProductController
from lib.controller.pos_order import PosOrder as PosOrderController
from lib.controller.pos_order_line import PosOrderLine as PosOrderLineController
from lib.controller.pos_payment import PosPayment as PosPaymentController
from lib.controller.pos_config import PosConfig as PosConfigController
from lib.controller.pos_session import PosSession as PosSessionController
from lib.controller.pos_category import PosCategory as PosCategoryController
from lib.controller.res_users import ResUsers as ResUserController

from qt_material import apply_stylesheet

import sys
import os
import logging 

logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(asctime)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Controller():

    is_login = False
    access_token = None
    pos_type = 'q'
    
    def __init__(self, app_path):
        super(Controller, self).__init__()
        self.app_path = app_path
        self.logger = logging.getLogger(__name__)
        
        #Init Value
        self.pos_order = False
        self.pos_session = False

        #Init Controller
        self.productProductController = ProductProductController(self)
        self.posOrderController = PosOrderController(self)
        self.posOrderLineController = PosOrderLineController(self)
        self.posPaymentController = PosPaymentController(self)
        self.posConfigController = PosConfigController(self)
        self.posSessionController = PosSessionController(self)
        self.posCategoryController = PosCategoryController(self)
        self.resUsersController = ResUserController(self)

    def load_ui(self):
        pass
        
    def load_login(self):     
        if self.pos_type == 'p':   
            from lib.view.pos_login import PosLoginUi

            self.posLoginUi = PosLoginUi(self)
            self.posLoginUi.show()

        if self.pos_type == 'q':
            from lib.view.q.pos_login import PosLoginUi

            self.posLoginUi = PosLoginUi(self)
            self.posLoginUi.show()

    def load_pos_command(self):
        if self.pos_type == 'q':
            from lib.view.q.pos_command import PosCommandUi
            self.posCommandUi = PosCommandUi(self)
            self.posLoginUi.close()
            self.posCommandUi.show()


    def load_pos_order(self):
        if self.pos_type == 'p':
            from lib.view.pos_order import PosOrderUi
            self.posOrderUi = PosOrderUi(self)
            self.posOrderUi.show()

        if self.pos_type == 'q':
            from lib.view.q.pos_order import PosOrderUi
            self.posOrderUi = PosOrderUi(self)
            self.posOrderUi.show()        

    def load_pos_order_line(self):
        if self.pos_type == 'q':
            from lib.view.q.pos_order_line import PosOrderLineUi
            self.posOrderLineUi = PosOrderLineUi(self)
            self.posOrderLineUi.show()

    def load_pos_payment(self):
        if self.pos_type == 'p':
            from lib.view.pos_payment import PosPaymentUi
            self.posPaymentUi = PosPaymentUi(self)
            self.posPaymentUi.show()
        
        if self.pos_type == 'q':
            from lib.view.q.pos_payment import PosPaymentUi
            self.posPaymentUi = PosPaymentUi(self)
            self.posPaymentUi.show()

    def load_pos_hold(self):
        if self.pos_type == 'p':
            pass
        if self.pos_type == 'q':
            from lib.view.q.pos_hold import PosHoldUi
            self.posHoldUi = PosHoldUi(self)
            self.posHoldUi.show()

    def load_pos_customer(self):
        self.posCustomerUi = PosCustomerUi(self)
        self.posCustomerUi.show()

    def load_pos_promo(self):
        self.posPromotionUi = PosPromotionUi(self)
        self.posPromotionUi.show()

    def load_pos_product(self):
        pass 

    def unload_pos_command(self):
        self.posCommandUi.close()
        self.posLoginUi.show()

    def unload_pos_order(self):
        self.posOrderUi.close()
        self.posCommandUi.show()
    
    def unload_pos_order_line(self):
        self.posOrderLineUi.close()

    def unload_pos_payment(self):
        self.posPaymentUi.close()
    
    def unload_pos_hold(self):
        self.posHoldUi.close()
    
    def unload_pos_customer(self):
        self.posCustomerUi.close()
        self.posOrderUi.setEnabled(True)
    
    def unload_pos_promotion(self):
        self.posPromotionUi.close()

    def logout(self):
        self.posOrderUi.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_yellow.xml')

    app_path = os.path.dirname(os.path.abspath(__file__))

    # stylesheet = app.styleSheet()
    # # app.setStyleSheet(stylesheet + "QPushButton{color: red; text-transform: none;}")
    # with open( app_path + '/style/custom.css') as file:
    #     app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    controller = Controller(app_path)
    controller.load_ui()
    controller.load_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
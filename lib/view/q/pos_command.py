from PyQt5 import QtWidgets, QtCore, QtSvg, uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox
import sys
import os
from lib.vendor.numpad import numberPopup
from lib.vendor.virtual_keyboard_controller import AlphaNeumericVirtualKeyboard
from lib.vendor.virtual_keyboard import KeyboardUI
from return_handling import ReturnHandling
from lib.view import *


class PosCommandUi(QtWidgets.QWidget):

    def __init__(self, controller):
        super(PosCommandUi, self).__init__()
        self.controller = controller
        self.app_path = controller.app_path
        print("Load Pos Command UI")

        #Load UI
        ui_path = os.path.join(self.app_path, "ui/q0003.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Command')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setOffset(20, 30)
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)
        
        #Init Ui
        self.initUi()
        self.initData()
    

    def initUi(self):
        self.ExitButton.clicked.connect(self.exitButtonPressed)
        self.TransactionButton.clicked.connect(self.transactionButtonPressed)
        self.CloseSessionButton.clicked.connect(self.closeSessionButtonPressed)
        self.HoldButton.clicked.connect(self.holdButtonPressed)
    
    def initData(self):
        returnHandling = self.controller.posConfigController.getLocalById(os.getenv("CONFIG_ID"))
        if not returnHandling.err:
            self.controller.config_id = returnHandling.data['result']
            self.controller.config_id['id']  = returnHandling.data['id']
            print(f'config_id : {self.controller.config_id}')
            #self.pos_session = self.posConfigController.open_session_cb(self.config_id['id'])
            returnHandling = self.controller.posSessionController.find_pos_session(self.controller.company_id,self.controller.config_id['id'],self.controller.uid)
            if not returnHandling.err:
                self.controller.pos_session = returnHandling.data['result']
                self.controller.pos_session['id'] = returnHandling.data['id']
                self.TransactionButton.setText(self.controller.pos_session['name'])
            else:
                self.controller.pos_session = False
                print("posSessionController.getActive: " + returnHandling.message)
        else:
            print("posConfigController.getLocalById: " + returnHandling.message)

    def transactionButtonPressed(self):
        self.controller.load_pos_order()

    def closeSessionButtonPressed(self):
        returnHandling = self.controller.posSessionController.close_pos_session(self.controller.company_id, self.controller.pos_session['id'])
        if not returnHandling.err:
            self.TransactionButton.setText('Transaction')
            self.controller.pos_session = False
            self.controller.unload_pos_command()
        else:
            msg = QMessageBox.about(self, "Warning", returnHandling.message)

    def exitButtonPressed(self):
        self.controller.unload_pos_command()

    def holdButtonPressed(self):
        self.controller.load_pos_hold()
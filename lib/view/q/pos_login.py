from PyQt5 import QtWidgets, QtCore, QtSvg, uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
from lib.vendor.numpad import numberPopup
from lib.vendor.virtual_keyboard_controller import AlphaNeumericVirtualKeyboard
from lib.vendor.virtual_keyboard import KeyboardUI
from return_handling import ReturnHandling
from lib.view import *

class PosLoginUi(QtWidgets.QWidget):

    def __init__(self, controller):
      super(PosLoginUi, self).__init__()
      self.controller = controller
      self.app_path = controller.app_path
      self.resUsersModel = ResUsersModel()

      #Load UI
      ui_path = os.path.join(self.app_path, "ui/q0002.ui")
      uic.loadUi(ui_path, self)
      self.setWindowTitle('Login')
      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
      self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
      self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
      effect = QtWidgets.QGraphicsDropShadowEffect(self)
      effect.setOffset(20, 30)
      effect.setBlurRadius(20)
      self.setGraphicsEffect(effect)


      #Init
      #self.connectlocaldb()
      self.initButton()
      #self.initTable()


      #Show
      #self.show()

    def initButton(self):
      self.EmailEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)
      self.PasswordEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)

      self.ExitButton.clicked.connect(self.exitButtonPressed)
      self.LoginButton.clicked.connect(self.loginButtonPressed)

    def exitButtonPressed(self):
      self.close()
    
    def getSession(self, user_id):
      returnHandling = self.posSess

    def loginButtonPressed(self):
      print('Login Button Pressed')
      returnHandling = self.controller.resUsersController.api_login('pos-dev', self.EmailEdit.text(), self.PasswordEdit.text())
      if returnHandling.err:
        self.showError(returnHandling.message)
        self.controller.logger.error(returnHandling.message)
        self.clearUi()
      else:
        print(returnHandling.message)
        username = self.EmailEdit.text()
        password = self.PasswordEdit.text()
        self.controller.logger.info(f'{username} login succesfully')
        data = returnHandling.data

        #Update Global Controller
        self.controller.is_login = True
        self.controller.access_token = data['access_token']
        self.controller.refresh_token = data['refresh_token']
        self.controller.logger.info("Login as " + username)
        self.controller.username = username
        self.controller.password = password
        self.controller.uid = 1
        self.controller.pos_session = False
        self.controller.company_id = 1    
        self.clearUi() 
        self.controller.load_pos_command()
       
    
    def emailNumpadButtonPressed(self):
      self.setEnabled(False)
      #self.exPopup = numberPopup(self, self.emailEdit, "", self.callBackOnSubmit, "Argument 1", "Argument 2")
      #self.exPopup.setGeometry(130, 320,400, 300)
      #self.exPopup.show()
      keyboard = AlphaNeumericVirtualKeyboard(self.emailEdit)
      keyboard.display(ui_Scroll=False)
    
    def showError(self, message):
        self.MessageLabel.setText(message)

    def clearUi(self):
        self.EmailEdit.setText("")
        self.PasswordEdit.setText("")
        self.EmailEdit.setFocus(True)
  
    def callBackOnSubmit(self, arg1, arg2): 
      print("Function is called with args: %s & %s" % (arg1, arg2))

    def onClick(self,e):
        self.setEnabled(True)
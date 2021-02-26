from PyQt5 import QtWidgets, QtCore, QtSvg, uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
from lib.vendor.numpad import numberPopup
from lib.vendor.virtual_keyboard_controller import AlphaNeumericVirtualKeyboard
from lib.vendor.virtual_keyboard import KeyboardUI
from return_handling import ReturnHandling
from lib.view. import *

#class PosLoginUi(QtWidgets.QDialog):
class PosLoginUi(QtWidgets.QWidget):

    def __init__(self, controller):
      super(PosLoginUi, self).__init__()
      self.controller = controller
      self.app_path = controller.app_path
      self.resUsersModel = ResUsersModel()
      self.resUsersController = ResUserController(self.controller)

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
      self.ExitButton.clicked.connect(self.exitButtonPressed)
      self.LoginButton.clicked.connect(self.loginButtonPressed)
      #self.EmailNumpadButton.clicked.connect(self.emailNumpadButtonPressed)

    def exitButtonPressed(self):
      self.close()
    
    def loginButtonPressed(self):
      print('Login Button Pressed')
      returnHandling = self.resUsersController.api_login( login=self.EmailEdit.text(), password=self.PasswordEdit.text())
      if returnHandling.err:
        print(returnHandling.message)
        self.messageLabel.setText("Invalid Email or Password")
        self.EmailEdit.setText("")
        self.PasswordEdit.setText("")
        self.EmailEdit.setFocus(True)
      else:
        print(returnHandling.message)
        data = returnHandling.data
        self.controller.is_login = True
        self.controller.access_token = data['access_token']
        self.controller.uid = data['uid']
        self.controller.company_id = data['company_id']
        self.controller.expires_in = data['expires_in']
        self.controller.load_pos_order()
    
    def emailNumpadButtonPressed(self):
      self.setEnabled(False)
      #self.exPopup = numberPopup(self, self.emailEdit, "", self.callBackOnSubmit, "Argument 1", "Argument 2")
      #self.exPopup.setGeometry(130, 320,400, 300)
      #self.exPopup.show()
      keyboard = AlphaNeumericVirtualKeyboard(self.emailEdit)
      keyboard.display(ui_Scroll=False)
    
    def callBackOnSubmit(self, arg1, arg2): 
      print("Function is called with args: %s & %s" % (arg1, arg2))

    def onClick(self,e):
        self.setEnabled(True)
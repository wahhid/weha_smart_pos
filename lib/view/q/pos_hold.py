from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize, Qt    

import sys
import os
import base64
import codecs
from functools import partial
from datetime import datetime
import hashlib
from escpos.printer import Usb
from lib.view import *

from dotenv import load_dotenv
import os

import re
import threading
import time


class PosOrder(QWidget):
   def __init__(self, pos_order_id):
      super(PosOrder, self).__init__()
      self.pos_order_id = pos_order_id

   def mousePressEvent(self, event):
      print("clicked " + str(self.pos_order_id))


class PosHoldUi(QWidget):
   
    def __init__(self, controller):
        super(PosHoldUi, self).__init__()
        self.controller = controller
        self.app_path = controller.app_path

        #Load UI
        ui_path = os.path.join(self.app_path, "ui/q0010.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Pos Order')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setOffset(20, 30)
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)  
        
        self.initUi()
        #self.initOrder()

    def initUi(self):
        self.TransactionVerticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.ExitButton.clicked.connect(self.exitButtonPressed)

    def initOrder(self):
        returnHandling = self.controller.posOrderController.getHold(self.controller.pos_session['id'])
        if not returnHandling.err:
            i = 0
            for pos_order in returnHandling.data['result']:
                pos_order.update({'id':  returnHandling.data['ids'][i]})
                self.add_pos_order(pos_order)
                i = i + 1

    def add_pos_order(self, pos_order):
        self.setCursor(Qt.WaitCursor)
        orderWidget =  PosOrder(pos_order['id'])
        ui_path = os.path.join(self.app_path, "ui/widget_order_q.ui")
        uic.loadUi(ui_path, orderWidget)
        productWidget.OrderNameLabel.setWordWrap(True)
        productWidget.OrderNameLabel.setText(pos_order['name'])
        productWidget.TotalLabel.setText(str(pos_order['amount_total']))
        
        #print("Add Product Widget")
        self.TransactionVerticalLayout.addWidget(orderWidget)
        scroll_bar = self.TransactionScrollArea.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.unsetCursor() 

    def exitButtonPressed(self):
        self.controller.unload_pos_hold()
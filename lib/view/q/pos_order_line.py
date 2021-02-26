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


class ProductLine(QWidget):
   def __init__(self, pos_order_line_id):
      super(ProductLine, self).__init__()
      self.pos_order_line_id = pos_order_line_id

   def mousePressEvent(self, event):
      print("clicked " + str(self.pos_order_line_id))


class PosOrderLineUi(QWidget):
   
    def __init__(self, controller):
        super(PosOrderLineUi, self).__init__()
        self.controller = controller
        self.app_path = controller.app_path

        #Controller   
        self.posOrderLineController = PosOrderLineController(self.controller)

        #Load UI
        ui_path = os.path.join(self.app_path, "ui/q0009.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Login')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setOffset(20, 30)
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)  
        
        self.initUi()
        self.initOrder()

    def initUi(self):
        self.TransactionVerticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.ExitButton.clicked.connect(self.exitButtonPressed)

    def initOrder(self):
        returnHandling = self.controller.posOrderLineController.getByOrderId(self.controller.posOrderUi.pos_order['id'])
        if not returnHandling.err:
            i = 0
            for pos_order_line in returnHandling.data['result']:
                pos_order_line.update({'id':  returnHandling.data['ids'][i]})
                self.add_product_line(pos_order_line)
                i = i + 1

    def add_product_line(self, pos_order_line):
        self.setCursor(Qt.WaitCursor)
        productWidget =  ProductLine(pos_order_line['id'])
        ui_path = os.path.join(self.app_path, "ui/widget_product_q.ui")
        uic.loadUi(ui_path, productWidget)
        productNameLabel = productWidget.findChild(QLabel, 'ProductNameLabel')
        productNameLabel.setWordWrap(True)
        productNameLabel.setText(pos_order_line['name'])
        productLstPriceLabel = productWidget.findChild(QLabel, 'ProductLstPriceLabel')
        productQtyLabel = productWidget.findChild(QLabel, 'ProductQtyLabel')
        productQtyLabel.setText(str(pos_order_line['qty']))
        totalLabel = productWidget.findChild(QLabel, 'TotalLabel')
        totalLabel.setText(str(pos_order_line['price_subtotal']))
        productImageLabel = productWidget.findChild(QLabel, 'ProductImageLabel')
        #productWidget.delProductLinePushButton.clicked.connect(partial(self.deleteProductLinePushButtonPressed, productWidget, pos_order_line))
        #productWidget.increasePushButton.clicked.connect(partial(self.increaseProductLinePushButtonPressed, productWidget, pos_order_line.id))
        #productWidget.decreasePushButton.clicked.connect(partial(self.decreaseProductLinePushButtonPressed, productWidget, pos_order_line.id))
        #if data[6]:
        #   image = QtGui.QPixmap() 
        #   image.loadFromData(base64.b64decode(str(data[6])))
        #   productImageLabel.setPixmap(image)
        
        #print("Add Product Widget")
        self.TransactionVerticalLayout.addWidget(productWidget)
        scroll_bar = self.TransactionScrollArea.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.unsetCursor() 

    def exitButtonPressed(self):
        self.controller.unload_pos_order_line()
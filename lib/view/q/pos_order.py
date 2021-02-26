
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    

import logging
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


class PosOrderUi(QWidget):
   
   def __init__(self, controller):
      super(PosOrderUi, self).__init__()
      self.controller = controller
      self.app_path = controller.app_path
      self.barcode = ""
      self.threads = list()
      self.pos_order = False
      load_dotenv(verbose=True)

      #Model
      #self.posLoginModel = PosLoginModel()
      self.productProductModel = ProductProductModel()
      self.posConfigModel = PosConfigModel()
      self.posCategoryModel = PosCategoryModel()
      self.resUsersModel = ResUsersModel()

      #Controller
      self.posConfigController = PosConfigController(self.controller)
      self.posSessionController = PosSessionController(self.controller)
      self.posOrderController = PosOrderController(self.controller)
      self.posOrderLineController = PosOrderLineController(self.controller)
      self.posPaymentController = PosPaymentController(self.controller)
      self.productProductController = ProductProductController(self.controller)
      self.posCategoryController = PosCategoryController(self.controller)
      self.resUsersController = ResUserController(self.controller)

      #Sync
      self.productProductSync = ProductProductSync(self.controller)
      self.posConfigSync = PosConfigSync(self.controller)
      self.posCategorySync = PosCategorySync(self.controller)
      self.resPartnerSync = ResPartnerSync(self.controller)
      #self.accountJournalSync = AccountJournalSync(self.controller)
      
      self.command = 'BRC'

      #Load UI
      ui_path = os.path.join(self.app_path, "ui/q0001.ui")
      uic.loadUi(ui_path, self)
      self.setWindowTitle('Order')
      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
      self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
      self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
      effect = QtWidgets.QGraphicsDropShadowEffect(self)
      effect.setOffset(20, 30)
      effect.setBlurRadius(20)
      self.setGraphicsEffect(effect)

      #Init
      self.initUi()
      
      #Init Order
      self.initOrder()
      self.enableUi()
      #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
      #self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
      #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
      #self.loadPosCategory()
      #self.loadProduct()
      #self.load_scrollarea()

      #self.initTable()

      #timer = QtCore.QTimer(self)
      #timer.timeout.connect(self.showTime)
      #timer.start(1000) # update every second
      #self.showTime()

      #Printer
      self.receipt01 = Receipt01()


   def initUi(self):
         
      #Style
      self.TotalLabel.setProperty('class', 'message_border')
      self.SessionLabel.setProperty('class', 'message_border')
      self.OperatorLabel.setProperty('class', 'message_border')
      self.CommandLabel.setProperty('class', 'message_border')
      
      self.PaymentButton.setProperty('class', 'pos_order_payment_button')
      #Command Button
      self.ProductButton.clicked.connect(self.productButtonPressed)
      self.PaymentButton.clicked.connect(self.checkOutButtonPressed)
      self.LineButton.clicked.connect(self.lineButtonPressed)
      self.ExitButton.clicked.connect(self.exitButtonPressed)
      self.HoldButton.clicked.connect(self.holdButtonPressed)

   def enableUi(self):
      #returnHandling = self.resUsersController.getById(self.controller.uid)
      #user = returnHandling.data
      #print(user)
      self.OperatorLabel.setText(self.controller.username)
      #self.commandEdit.setEnabled(True)
   

   def disableUi(self):
      #user = self.posLoginModel.getUserInfo()
      self.OperatorLabel.setText('Not Login')
      #self.commandEdit.setEnabled(True)

      self.customerButton.setEnabled(False)
      #self.productButton.setEnabled(True)
      self.promoButton.setEnabled(False)
      self.holdButton.setEnabled(False)
      self.barcodeButton.setEnabled(False)
      self.priceButton.setEnabled(False)
      self.qtyButton.setEnabled(False)
      self.discButton.setEnabled(False)
      self.syncButton.setEnabled(False)
      self.checkOutButton.setEnabled(False)
      
   def showTime(self):
      displayTxt =datetime.now().strftime('%d-%m-%Y %H:%M:%S')
      self.clockLabel.setText(displayTxt)

   def initOrder(self):
      #self.pos_session = self.posConfigController.open_session_cb(self.config_id['id'])
      if not self.controller.pos_session:
         #returnHandling = self.posSessionController.getActive(self.controller.company_id,self.controller.config_id['id'],self.controller.uid)
         returnHandling = self.posSessionController.create_pos_session(self.controller.company_id, self.controller.config_id['id'], 1, self.controller.uid)
         if not returnHandling.err:
            self.controller.pos_session = returnHandling.data['result'][0]
            self.controller.pos_session.update({'id':returnHandling.data['ids'][0]})
      else:
         self.SessionLabel.setText(self.controller.pos_session['name'])
         returnHandling = self.posOrderController.find_pos_order(self.controller.pos_session['id'], self.controller.uid)
         print(returnHandling.data)
         if not returnHandling.err:
            print(returnHandling.message)
            self.pos_order = returnHandling.data['result']
            self.pos_order.update({'id': returnHandling.data['id']})
            print("POS ORDER")
            print(self.pos_order)
            #self.pos_order = self.posOrderController.create_pos_order(self.pos_session['id'])
            self.PaymentButton.setText(self.pos_order['name'])
            #status, message, pos_order_lines = self.posOrderLineController.getByOrderId(self.pos_order.id)
            #for pos_order_line in pos_order_lines:
            #   print(pos_order_line)
            self.getSummary()
            self.updateTotalLabel()
         else:
            print(returnHandling.message)

   def validation_barcode(self, input_string):
      regex = re.compile('^[0-9]{10}$', re.I)
      match = regex.match(str(input_string))
      return bool(match)

   def add_order_line(self, product, qty=1):
      if not self.pos_order:
         returnHandling = self.posOrderController.find_pos_order(self.controller.pos_session['id'], self.controller.uid)
         if not returnHandling.err:
            self.pos_order = returnHandling.data['result']
            self.pos_order['id'] = returnHandling.data['id']
         else:
            print("Error Create Pos Orde")

      if self.pos_order:
         print(self.pos_order)
         self.PaymentButton.setText(self.pos_order['name'])
         #Prepare for Create Pos Order Line
         print("ADD ORDER LINE")
         print(product)
         print(product.get('id'))
         self._prepare_pos_order_line(product)
         returnHandling = self.posOrderLineController.create_order_line(self.pos_order_line)
         if not returnHandling.err:
            pos_order_line = returnHandling.data['result']
            pos_order_line.update({"id": returnHandling.data['id']})
            print(pos_order_line)
            self.add_product_line(pos_order_line)
            self.getSummary()
            self.updateTotalLabel()
         else:
            print(returnHandling.message)

   def add_product_line(self, pos_order_line):
      self.ProductLabel.setText(pos_order_line['name'])
      self.PriceLabel.setText("@ " + str(pos_order_line['price_subtotal']))
      self.QuantityButton.setText(str(pos_order_line['qty']) + " pcs")
      self.LineTotalLabel.setText(str(pos_order_line['price_subtotal']))

   def deleteProductLinePushButtonPressed(self, widget, data):
      print("Delete Payment Widget")
      requestHandling = self.posOrderLineController.localDelete(data)
      if not requestHandling.err:
         widget.deleteLater()
         self.get_due()
         msg = QMessageBox.about(self, "Warning", requestHandling.message)
   
   def increaseProductLinePushButtonPressed(self, widget, id):
      returnHandling = self.posOrderLineController.getLocalById(id)
      if not returnHandling.err:
         pos_order_line = returnHandling.data
         pos_order_line.qty = pos_order_line.qty + 1
         pos_order_line.price_subtotal = pos_order_line.price_unit *  pos_order_line.qty
         returnHandling = self.posOrderLineController.localUpdate(pos_order_line)
         if not returnHandling.err:
            pos_order_line  = returnHandling.data
            widget.ProductQtyLabel.setText(str(pos_order_line.qty))
            widget.TotalLabel.setText(str(pos_order_line.price_subtotal))
            self.getSummary()
            self.updateTotalLabel()
         else:
            msg = QMessageBox.about(self, "Warning", requestHandling.message)

   def decreaseProductLinePushButtonPressed(self, widget, id):
      returnHandling = self.posOrderLineController.getLocalById(id)
      if not returnHandling.err:
         pos_order_line = returnHandling.data
         if pos_order_line.qty > 1:
            pos_order_line.qty = pos_order_line.qty - 1
            pos_order_line.price_subtotal = pos_order_line.price_unit *  pos_order_line.qty
            returnHandling = self.posOrderLineController.localUpdate(pos_order_line)
            if not returnHandling.err:
               pos_order_line  = returnHandling.data
               widget.ProductQtyLabel.setText(str(pos_order_line.qty))
               widget.TotalLabel.setText(str(pos_order_line.price_subtotal))
               self.getSummary()
               self.updateTotalLabel()
               msg = QMessageBox.about(self, "Warning", requestHandling.message)

   def updateTotalLabel(self):
      self.TotalLabel.setText(str(self.summary['total_order_line']))

   def getSummary(self):
      returnHandling = self.posOrderController.getSummary(self.pos_order['id'])
      if not returnHandling.err:
         print(returnHandling)
         self.summary = returnHandling.data['data']
      else:
         print(f'getTotalByOrderId: {returnHandling.message}')
         self.summary = {
            'total_order_line': 0,
            'total_payment': 0,
         }

   def getOrderSummary(self):
      returnHandling = self.posOrderLineController.getTotalByOrderId(self.pos_order['id'])
      if not returnHandling.err:
         print(f'getTotalByOrderId : {returnHandling.data}')
         self.order_summary = returnHandling.data
      else:
         print(f'getTotalByOrderId: {returnHandling.message}')
         self.order_summary = {
            'amount_paid': 0,
            'amount_total': 0,
         }

   def getPaymentSummary(self):
      returnHandling = self.posPaymentController.getTotalByOrderId(self.pos_order['id'])
      if not returnHandling.err:
         self.payment_summary = returnHandling.data
      else:
         print(f'getTotalByOrderId: {returnHandling.message}')
         self.payment_summary = {
            'amount_paid': 0,
            'amount_total': 0,
         }

   def get_due(self):
      self.getSummary()
      return self.summary['total_order_line'] - self.summary['total_payment']

   def clear_product_line(self):
      #for i in range(self.transactionVerticalLayout.count()): self.transactionVerticalLayout.itemAt(i).widget().close()
      pass 

   def keyPressEvent(self, event):
      if self.controller.is_login:
         if event.key() == QtCore.Qt.Key_Asterisk:
            print("Detect QTY Command")
            self.command = "QTY"
         elif event.key() == QtCore.Qt.Key_Return:
            if self.command == 'BRC':
               if self.validation_barcode(self.barcode): 
                  returnHandling = self.productProductController.getByBarcode(self.barcode)
                  if not returnHandling.err:
                     if len(returnHandling.data['result']) > 0:
                        product = returnHandling.data['result'][0]
                        product.update({'id':returnHandling.data['ids'][0]})
                        self.add_order_line(product)
                        print("Add order Line")
                     else:
                        print("Not Match")
                        dialog = QMessageBox(self)
                        dialog.setWindowTitle('Warning')
                        dialog.setText('Product not found')
                        dialog.setIcon(QMessageBox.Warning)
                        dialog.show()
                  else:
                     print("Product not Found")
                     dialog = QMessageBox(self)
                     dialog.setWindowTitle('Warning')
                     dialog.setText('Product not Found')
                     dialog.setIcon(QMessageBox.Warning)
                     dialog.show()
               else:
                  print("Not Match")
                  dialog = QMessageBox(self)
                  dialog.setWindowTitle('Warning')
                  dialog.setText('Barcode not match')
                  dialog.setIcon(QMessageBox.Warning)
                  # dialog.setDetailedText("Barcode must be 13 character")
                  # dialog.resize(200,64)
                  dialog.show()


            self.barcode = ""
            self.CommandLabel.setText("")
         else:
            self.barcode = self.barcode + event.text()
            self.CommandLabel.setText(self.CommandLabel.text() + event.text())
      
   def _prepare_pos_order_line(self, product, qty=1):
      self.pos_order_line = {
         'company_id': 0,
         'name': product['display_name'],
         'notice': "",
         'product_id': product['id'],
         'price_unit': product['lst_price'],
         'qty' : qty,
         'price_subtotal': qty * product['lst_price'],
         'price_subtotal_incl': qty * product['lst_price'],
         'discount': 0,
         'order_id': self.pos_order['id'],
         'product_uom_id': 1,
         'currency_id': 12,
         'tax_id': 0
      }
      
   def checkLogin(self, username, password):
      result = self.posLoginModel.login(username, password)
      return result

   def setCustomer(self, customer):
      prin("Set Customer")
      pass

   #Print
   def printReceipt(self, pos_order_id):
      returnHandling = self.posOrderController.getById(pos_order_id)
      if not returnHandling.err:
         pos_order = returnHandling.data
         returnHandling = self.posOrderLineController.getByOrderId(pos_order['id'])
         if not returnHandling.err:
            pos_order_lines = returnHandling.data
            try:
               self.receipt01.print(pos_order, pos_order_lines)
            except Exception as e:
               dialog = QMessageBox(self)
               dialog.setWindowTitle('Warning')
               dialog.setText('Printer Error or not Found')
               dialog.setIcon(QMessageBox.Warning)
               dialog.show()
         else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle('Warning')
            dialog.setText('Order line empty')
            dialog.setIcon(QMessageBox.Warning)
            dialog.show()
      else:
            dialog = QMessageBox(self)
            dialog.setWindowTitle('Warning')
            dialog.setText('Order not found')
            dialog.setIcon(QMessageBox.Warning)
            dialog.show()

   #Button Pressed
   def customerButtonPressed(self):
      print('Customer Button Pressed')
      self.controller.load_pos_customer()

   def promoButtonPressed(self):
      print('Promo Button Pressed')
      self.controller.load_pos_promo()

   def productButtonPressed(self):
      print('Product Button Pressed')
          
   def paymentButtonPressed(self):
      print('Payment Button Pressed')
      self.controller.load_pos_payment()

   def lineButtonPressed(self):
      self.controller.load_pos_order_line()

   def holdButtonPressed(self):
      print("Hold Button Pressed")
      #Change Pos Order to hold

      #Create New Pos Order
      #Clear View

   def exitButtonPressed(self):
      print('Exit Button Pressed')
      self.controller.unload_pos_order()
      
      
   def checkOutButtonPressed(self):
      print('Checkout Button Pressed')
      if self.pos_order:
         self.controller.load_pos_payment()
      else:
         print("No Pos Order")
         dialog = QMessageBox(self)
         dialog.setWindowTitle('Warning')
         dialog.setText("No Pos Order Transaction")
         dialog.setIcon(QMessageBox.Warning)
         dialog.show()
      #self.setCursor(QCursor(QtCore.Qt.WaitCursor))
      # self.posOrderController.setPaid(self.pos_order.id)
      # pos_order_json = self.posOrderController.getJson(self.pos_order.id)
      # print(pos_order_json)
      # self.pos_order = self.posOrderController.create_pos_order(self.pos_session['id'])
      # self.orderLabel.setText(self.pos_order.name)
      # self.totalLabel.setText("0.0")
      # self.transactionTable.setRowCount(0)
      #self.setCursor()

   def syncButtonPressed(self):
      print('Sync Button Pressed ')
      self.productProductSync.sync()
      #self.resPartnerSync.sync()
      #self.posConfigSync.sync()
      #self.posCategorySync.sync()
      #self.accountJournalSync()

   def logoutButtonPressed(self):
      print('Logout Button Pressed')
      if self.controller.is_login:
         self.controller.logout()
         #self.setEnabled(False)
         #dlg = PosLoginUi(self, self.app_path)
         #dlg.setWindowModality(QtCore.Qt.ApplicationModal)
         #if dlg.exec_():
         #   print("Success!")
         #else:
         #   print("Cancel!")

   def posCategoryButtonPressed(self, data):
        self.pos_category_id = data.id
        #print(self.pos_category_id)

   def posProductButtonPressed(self, data={}):
         self.pos_product = data['id']
         print(self.pos_product)
         barcode = data['barcode']
         status, message, product = self.productProductController.getProductById(data['id'], False)
         if not status:
            print(product)
            self.add_order_line(product)
         else:
            print(message)
            dialog = QMessageBox(self)
            dialog.setWindowTitle('Warning')
            dialog.setText(message)
            dialog.setIcon(QMessageBox.Warning)
            dialog.show()

   def posHoldPushButtonPressed(self):
      pass
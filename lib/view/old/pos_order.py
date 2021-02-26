from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
import base64
import codecs
from functools import partial
from datetime import datetime
import hashlib
from escpos.printer import Usb
from . import *

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
      self.threads = list()
      load_dotenv(verbose=True)

      #Model
      #self.posLoginModel = PosLoginModel()
      self.productProductModel = ProductProductModel()
      self.posConfigModel = PosConfigModel()
      self.posCategoryModel = PosCategoryModel()
      self.resUsersModel = ResUsersModel()

      #Controller
      # self.posConfigController = PosConfigController(self.controller)
      # self.posOrderController = PosOrderController(self.controller)
      # self.posOrderLineController = PosOrderLineController(self.controller)
      # self.posPaymentController = PosPaymentController(self.controller)
      # self.productProductController = ProductProductController(self.controller)
      # self.posCategoryController = PosCategoryController(self.controller)
      # self.resUsersController = ResUserController(self.controller)

      #Sync
      self.productProductSync = ProductProductSync(self.controller)
      self.posConfigSync = PosConfigSync(self.controller)
      self.posCategorySync = PosCategorySync(self.controller)
      self.resPartnerSync = ResPartnerSync(self.controller)
      #self.accountJournalSync = AccountJournalSync(self.controller)
      
      self.command = 'BRC'

      #Load UI
      self.ui = 1
      if self.ui == 0: 
         ui_path = os.path.join(self.app_path, "ui/p0001.ui")
      else:
         ui_path = os.path.join(self.app_path, "ui/p0001_list.ui")

      uic.loadUi(ui_path, self)
   
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
      #Init Label
      self.sessionLabel = self.findChild(QLabel, 'SessionLabel')
      self.orderLabel = self.findChild(QLabel, 'OrderLabel')
      self.operatorLabel = self.findChild(QLabel, 'OperatorLabel')
      self.clockLabel = self.findChild(QLabel, 'ClockLabel')
      self.totalLabel = self.findChild(QLabel, 'TotalLabel')
      self.commandLabel = self.findChild(QLabel, 'CommandLabel')
      self.commandLabel.setText("")

      #Init Scorll Area
      self.transactionScrollArea = self.findChild(QScrollArea, 'TransactionScrollArea')
      self.transactionVerticalLayout = self.findChild(QVBoxLayout, 'TransactionVerticalLayout')
      self.transactionVerticalLayout.setAlignment(QtCore.Qt.AlignTop)

      #Init ListView
      #self.transactionListView = self.findChild(QListView, 'TransactionListView')

      #Init Category Button
      if self.ui == 0:
         self.homeCategoryPushButton = self.findChild(QPushButton, 'HomeCategoryPushButton')
         self.posCategory01PushButton = self.findChild(QPushButton, 'PosCategory01PushButton')
         self.posCategory02PushButton = self.findChild(QPushButton, 'PosCategory02PushButton')
         self.posCategoryOtherPushButton = self.findChild(QPushButton, 'PosCategoryOtherPushButton')

      #Init Product Button
      if self.ui == 0:
         self.posProduct01PushButton = self.findChild(QPushButton, 'PosProduct01PushButton')
         self.posProduct02PushButton = self.findChild(QPushButton, 'PosProduct02PushButton')
         self.posProduct03PushButton = self.findChild(QPushButton, 'PosProduct03PushButton')
         self.posProduct04PushButton = self.findChild(QPushButton, 'PosProduct04PushButton')
         self.posProduct05PushButton = self.findChild(QPushButton, 'PosProduct05PushButton')
         self.posProduct06PushButton = self.findChild(QPushButton, 'PosProduct06PushButton')
         
      #Command Button
      self.checkOutButton = self.findChild(QPushButton, 'CheckoutButton')
      self.checkOutButton.clicked.connect(self.checkOutButtonPressed)

      #self.loginButton = self.findChild(QPushButton, 'LoginButton')
      self.logoutButton.clicked.connect(self.logoutButtonPressed)

      self.customerButton = self.findChild(QPushButton, 'CustomerButton')
      self.customerButton.clicked.connect(self.customerButtonPressed)

      #self.productButton = self.findChild(QPushButton, 'ProductButton')
      #self.productButton.clicked.connect(self.productButtonPressed)

      self.promoButton = self.findChild(QPushButton, 'PromoButton')
      self.promoButton.clicked.connect(self.promoButtonPressed)

      self.holdButton = self.findChild(QPushButton, 'HoldPushButton')
      self.barcodeButton = self.findChild(QPushButton, 'BarcodePushButton')
      self.priceButton = self.findChild(QPushButton, 'PricePushButton')
      self.qtyButton = self.findChild(QPushButton, 'QtyPushButton')
      self.discButton = self.findChild(QPushButton, 'DiscPushButton')
      
      self.syncButton = self.findChild(QPushButton, 'SyncPushButton')
      self.syncButton.clicked.connect(self.syncButtonPressed)

   def loadPosCategory(self):
      err , message, pos_categories = self.controller.posCategoryController.getLocalAll()
      print("Load POS Categories")
      print(pos_categories)
      if pos_categories is not None:
         self.posCategory01PushButton.setText(pos_categories[0].name)
         self.posCategory01PushButton.clicked.connect(partial(self.posCategoryButtonPressed, data=pos_categories[0]))
         self.posCategory02PushButton.setText(pos_categories[1].name)
         self.posCategory02PushButton.clicked.connect(partial(self.posCategoryButtonPressed, data=pos_categories[1]))

   def loadProduct(self):
      products = self.controller.productProductController.getProducts(True)
      print("Load POS Products")
      print(products)
      self.posProduct01PushButton.setText(products[0]['name'])
      self.posProduct01PushButton.clicked.connect(partial(self.posProductButtonPressed, data=products[0]))
      self.posProduct02PushButton.setText(products[1]['name'])
      self.posProduct02PushButton.clicked.connect(partial(self.posProductButtonPressed, data=products[1]))
      self.posProduct03PushButton.setText(products[2]['name'])
      self.posProduct03PushButton.clicked.connect(partial(self.posProductButtonPressed, data=products[2]))
      self.posProduct04PushButton.setText(products[3]['name'])
      self.posProduct04PushButton.clicked.connect(partial(self.posProductButtonPressed, data=products[3]))
      self.posProduct05PushButton.setText(products[4]['name'])
      self.posProduct05PushButton.clicked.connect(partial(self.posProductButtonPressed, data=products[4]))
      self.posProduct06PushButton.setText(products[5]['name'])
      self.posProduct06PushButton.clicked.connect(partial(self.posProductButtonPressed, data=products[5]))
   
   def load_scrollarea(self):   
      print("Add Product Widget")
      
      for i in range(1,100):
         productWidget = QWidget()
         ui_path = os.path.join(self.app_path, "ui/widget_product.ui")
         #ui_path = "../../ui/widget_product.ui"
         uic.loadUi(ui_path, productWidget)
         print("Add Product Widget")
         self.transactionVerticalLayout.addWidget(productWidget)
      
      #Scroll Area Properties
      #self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
      #self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
      #self.scroll.setWidgetResizable(True)
      #self.scroll.setWidget(self.widget)

   def enableUi(self):
      returnHandling = self.resUsersController.getById(self.controller.uid)
      user = returnHandling.data
      print(user)
      self.operatorLabel.setText(user['name'])
      #self.commandEdit.setEnabled(True)
      if self.ui == 0:
         self.homeCategoryPushButton.setEnabled(True)
         self.posCategory01PushButton.setEnabled(True)
         self.posCategory02PushButton.setEnabled(True)
         self.posCategoryOtherPushButton.setEnabled(True)

         self.posProduct01PushButton.setEnabled(True)
         self.posProduct02PushButton.setEnabled(True)
         self.posProduct03PushButton.setEnabled(True)
         self.posProduct04PushButton.setEnabled(True)
         self.posProduct05PushButton.setEnabled(True)
         self.posProduct06PushButton.setEnabled(True)

      self.customerButton.setEnabled(True)
      #self.productButton.setEnabled(True)
      self.promoButton.setEnabled(True)
      self.holdButton.setEnabled(True)
      self.barcodeButton.setEnabled(True)
      self.priceButton.setEnabled(True)
      self.qtyButton.setEnabled(True)
      self.discButton.setEnabled(True)
      self.syncButton.setEnabled(True)
      self.checkOutButton.setEnabled(True)

      if self.ui == 0:
         self.loadPosCategory()
         #self.loadProduct()
         #self.load_scrollarea()

   def disableUi(self):
      #user = self.posLoginModel.getUserInfo()
      self.operatorLabel.setText('Not Login')
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

   def initTable(self):
      self.transactionTable = self.findChild(QtWidgets.QTableWidget, 'TransactionTableWidget')
      # #self.orderTableData = 
      self.transactionTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows); 
      self.transactionTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
      self.transactionTable.setColumnCount(6)
      self.transactionTable.setRowCount(0)
      self.transactionTable.setHorizontalHeaderLabels(['No','Product Name','Qty','Price', 'Discount', 'Total'])
      self.transactionTable.setWordWrap(True)
      header = self.transactionTable.horizontalHeader()       
      header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
      #self.transactionTableView.setModel(self.posOrderLineTableModel)
      self.transactionTable.setColumnWidth (0, 30);

   def initOrder(self):
      self.config_id = self.posConfigController.getById(os.getenv("CONFIG_ID"))
      if self.config_id:
         self.pos_session = self.posConfigController.open_session_cb(self.config_id['id'])
         if self.pos_session:
            self.sessionLabel.setText(self.pos_session['name'])
            self.pos_order = self.posOrderController.find_pos_order()
            if self.pos_order:
               #self.pos_order = self.posOrderController.create_pos_order(self.pos_session['id'])
               self.orderLabel.setText(self.pos_order.name)
               status, message, pos_order_lines = self.posOrderLineController.getByOrderId(self.pos_order.id)
               for pos_order_line in pos_order_lines:
                  print(pos_order_line)
                  self.add_product_line(pos_order_line)
                  #product_remote = self.productProductController.getProductById(pos_order_line.product_id, False)
                  #print(type(product_remote['image_1920']))
                  #image_data_decode = codecs.decode(product_remote['image_1920'], "base64")
                  #image_data_decode = bytes(product_remote['image_1920'].encode('ascii'))
                  #print(image_data_decode)
                  #line = ['1', pos_order_line.name, 1, pos_order_line.price_unit , 0, pos_order_line.price_subtotal]
                  #self.add_product_line(line)
               #self.totalLabel.setText(str(self.posOrderLineController.getTotalByOrderId(self.pos_order.id)))
         else:
            msg = QMessageBox.about(self, "Warning", "POS Session Error")
      else:
          msg = QMessageBox.about(self, "Warning", "POS Config Error")

   def validation_barcode(self, input_string):
      regex = re.compile('^[0-9]{10}$', re.I)
      match = regex.match(str(input_string))
      return bool(match)

   def add_row(self, data):
      print("add row")
      numRows = self.transactionTable.rowCount()
      self.transactionTable.insertRow(numRows)
      self.transactionTable.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(data[0])))
      self.transactionTable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(data[1] + '\n' + str(data[1]))))
      item =  QtWidgets.QTableWidgetItem(str(data[2]))
      item.setTextAlignment(QtCore.Qt.AlignCenter)
      self.transactionTable.setItem(numRows, 2, item)
      item =  QtWidgets.QTableWidgetItem(str(data[3]))
      item.setTextAlignment(QtCore.Qt.AlignRight)
      self.transactionTable.setItem(numRows, 3, item)
      item =  QtWidgets.QTableWidgetItem(str(data[4]))
      item.setTextAlignment(QtCore.Qt.AlignCenter)
      self.transactionTable.setItem(numRows, 4, item)
      item =  QtWidgets.QTableWidgetItem(str(data[5]))
      item.setTextAlignment(QtCore.Qt.AlignRight)
      self.transactionTable.setItem(numRows, 5, QtWidgets.QTableWidgetItem(item))
      self.transactionTable.selectRow(numRows)
      #self.calculateTotal()

   def add_order_line(self, product, qty=1):
      if not self.pos_order:
         self.pos_order = self.posOrderController.create_pos_order(self.pos_session['id'])
         self.orderLabel.setText(self.pos_order.name)

      #Prepare for Create Pos Order Line
      self._prepare_pos_order_line(product)
      status, message, pos_order_line = self.posOrderLineController.insert_order_line(self.pos_order_line)
      if not status:
         print(pos_order_line)
         self.add_product_line(pos_order_line)
         self.totalLabel.setText(str(self.posOrderLineController.getTotalByOrderId(self.pos_order.id)))
      else:
         print(message)

   def add_product_line(self, pos_order_line):
      productWidget =  ProductLine(pos_order_line.id)
      ui_path = os.path.join(self.app_path, "ui/widget_product.ui")
      uic.loadUi(ui_path, productWidget)
      productNameLabel = productWidget.findChild(QLabel, 'ProductNameLabel')
      productNameLabel.setWordWrap(True)
      productNameLabel.setText(pos_order_line.name)
      productLstPriceLabel = productWidget.findChild(QLabel, 'ProductLstPriceLabel')
      productQtyLabel = productWidget.findChild(QLabel, 'ProductQtyLabel')
      productQtyLabel.setText(str(pos_order_line.qty))
      totalLabel = productWidget.findChild(QLabel, 'TotalLabel')
      totalLabel.setText(str(pos_order_line.price_subtotal))
      productImageLabel = productWidget.findChild(QLabel, 'ProductImageLabel')
      productWidget.delProductLinePushButton.clicked.connect(partial(self.deleteProductLinePushButtonPressed, productWidget, pos_order_line))
      productWidget.increasePushButton.clicked.connect(partial(self.increaseProductLinePushButtonPressed, productWidget, pos_order_line.id))
      productWidget.decreasePushButton.clicked.connect(partial(self.decreaseProductLinePushButtonPressed, productWidget, pos_order_line.id))
      #if data[6]:
      #   image = QtGui.QPixmap() 
      #   image.loadFromData(base64.b64decode(str(data[6])))
      #   productImageLabel.setPixmap(image)
      
      print("Add Product Widget")
      self.transactionVerticalLayout.addWidget(productWidget)
      scroll_bar = self.transactionScrollArea.verticalScrollBar()
      scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))

   def deleteProductLinePushButtonPressed(self, widget, data):
      print("Delete Payment Widget")
      requestHandling = self.posOrderLineController.localDelete(data)
      if not requestHandling.err:
         widget.deleteLater()
         self.totalLabel.setText(str(self.posOrderLineController.getTotalByOrderId(self.pos_order.id)))
      else:
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
            self.totalLabel.setText(str(self.posOrderLineController.getTotalByOrderId(self.pos_order.id)))
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
               self.totalLabel.setText(str(self.posOrderLineController.getTotalByOrderId(self.pos_order.id)))
            else:
               msg = QMessageBox.about(self, "Warning", requestHandling.message)

   def get_due(self):
      total_order = self.posOrderLineController.getTotalByOrderId(self.pos_order.id)
      total_payment = self.posPaymentController.getTotalByOrderId(self.pos_order.id)
      return total_order - total_payment

   def clear_product_line(self):
      for i in range(self.transactionVerticalLayout.count()): self.transactionVerticalLayout.itemAt(i).widget().close()

   def keyPressEvent(self, event):
      if self.controller.is_login:
         if event.key() == QtCore.Qt.Key_Asterisk:
            print("Detect QTY Command")
            self.command = "QTY"
         elif event.key() == QtCore.Qt.Key_Return:
            #self.proceed()
            print("Enter") 
            print(self.commandLabel.text())     
            #self.commandEdit.setText(event.text())
            if self.command == 'BRC':
               if self.validation_barcode(self.commandLabel.text()): 
                  product = self.productProductController.getLocalByBarcode(self.commandLabel.text())
                  if product is not None:
                     self.add_order_line(product)
                  else:
                     print("Product not Found")
                     dialog = QMessageBox(self)
                     dialog.setWindowTitle('Warning')
                     dialog.setText('Product not Found')
                     dialog.setIcon(QMessageBox.Warning)
                     dialog.setDetailedText("The details are as follows:")
                     dialog.resize(400, 200)
                     dialog.show()
               else:
                  print("Not Match")

                  dialog = QMessageBox(self)
                  dialog.setWindowTitle('Warning')
                  dialog.setText('Barcode not match')
                  dialog.setIcon(QMessageBox.Warning)
                  dialog.setDetailedText("Barcode must be 13 character")
                  dialog.resize(200,64)
                  dialog.show()


            self.commandLabel.setText("")
         else:
            self.commandLabel.setText(self.commandLabel.text() + event.text())    
      
   def _prepare_pos_order_line(self, product, qty=1):
      self.pos_order_line = {
         'company_id': 0,
         'name': product.display_name,
         'notice': "",
         'product_id': product.id,
         'price_unit': product.lst_price,
         'qty' : qty,
         'price_subtotal': qty * product.lst_price,
         'price_subtotal_incl': qty * product.lst_price,
         'discount': 0,
         'order_id': self.pos_order.id,
         'product_uom_id': 1,
         'currency_id': 12,
         'tax_id': 0
      }
      # if local:
      #    #order_line = ['1',product.name, 1, product.lst_price , 0, 1 *  product.lst_price]
      #    self.pos_order_line = {
      #       'company_id': 0,
      #       'name': product.name,
      #       'notice': "",
      #       'product_id': product.id,
      #       'price_unit': product.lst_price,
      #       'qty' : qty,
      #       'price_subtotal': qty * product.lst_price,
      #       'price_subtotal_incl': qty * product.lst_price,
      #       'discount': 0,
      #       'order_id': self.pos_order.id,
      #       'product_uom_id': 1,
      #       'currency_id': 12,
      #       'tax_id': 0
      #    }
      # else:
      #    #self.order_line = ['1',product['display_name'], 1, product['lst_price'] , 0, 1 *  product['lst_price']]
      #    self.pos_order_line = {
      #       'company_id': 0,
      #       'name': product['display_name'],
      #       'notice': "",
      #       'product_id': product['id'],
      #       'price_unit': product['lst_price'],
      #       'qty' : qty,
      #       'price_subtotal': qty * product['lst_price'],
      #       'price_subtotal_incl': qty * product['lst_price'],
      #       'discount': 0,
      #       'order_id': self.pos_order.id,
      #       'product_uom_id': 1,
      #       'currency_id': 12,
      #       'tax_id': 0
      #    } 

   def checkLogin(self, username, password):
      result = self.posLoginModel.login(username, password)
      return result

   def setCustomer(self, customer):
      prin("Set Customer")
      pass

   #Print
   def printReceipt(self, pos_order_id):
      status, message, pos_order = self.posOrderController.getById(pos_order_id, local=True)
      if not status:
         print(pos_order)
         status, message, pos_order_lines = self.posOrderLineController.getByOrderId(pos_order.id, local=True)
         if not status:
            print(pos_order_lines)
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
          
   def checkOutButtonPressed(self):
      print('Checkout Button Pressed')
      if self.pos_order:
         self.controller.pos_order_id  = self.pos_order.id
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
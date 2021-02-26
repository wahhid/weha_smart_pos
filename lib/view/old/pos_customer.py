from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
from functools import partial

#Controller
from lib.controller.res_partner import ResPartner as ResPartnerController

#Vendor
from lib.vendor.virtual_keyboard_controller import *
from lib.vendor.virtual_keyboard import *


class CustomerLine(QWidget):
   def __init__(self, customer_id):
      super(CustomerLine, self).__init__()
      self.customer_id = customer_id

   def mousePressEvent(self, event):
      print("clicked " + str(self.customer_id))

class PosCustomerUi(QtWidgets.QDialog):

    def __init__(self, controller):
        super(PosCustomerUi, self).__init__()
        self.controller = controller
        self.customer_id = False
        
        self.initUi()
        self.prevPushButtonPressed()
        #self.getCustomers()
        #self.fillCustomers()

    def initUi(self):
        ui_path = os.path.join(self.controller.app_path, "ui/pos_customer.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Customers')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.page_number = 1
        self.row_number = 6
        self.pagination = False

        #Controller
        self.resPartnerController = ResPartnerController(self.controller)

        #Scroll Area
        self.customerScrollArea = self.findChild(QScrollArea, "CustomerScrollArea")

        #Vertical Layout
        self.customerGridLayout = self.findChild(QGridLayout, "CustomerGridLayout")

        self.keyboardPushButton = self.findChild(QPushButton, "KeyboardPushButton")
        #self.keyboardPushButton.clicked.connect(self.keyboardPushButtonPressed)

        self.searchCustomerLineEdit = self.findChild(QLineEdit, "SearchCustomerLineEdit")
        #self.searchCustomerLineEdit.textEdited.connect(self.searchCustomer)
        #self.keyboard = VKQLineEdit(self.searchCustomerLineEdit)

        self.exitPushButton.clicked.connect(self.exitPushButtonPressed)
        self.prevPushButton.clicked.connect(self.prevPushButtonPressed)
        self.nextPushButton.clicked.connect(self.nextPushButtonPressed)
        
    def getCustomers(self):
        self.customers = self.resPartnerController.getLocalAll()

    def clear_customer_grid(self):
      for i in range(self.customerGridLayout.count()): self.customerGridLayout.itemAt(i).widget().close()

    def fillCustomers(self):
        #customers = self.resPartnerController.getLocalAll()
        col_count=1
        row = 0
        col = 0 
        for customer in self.customers:
            print(customer)
            self._add_customer(customer, row, col)
            col = col + 1
            if col > col_count:
                col = 0
                row = row + 1
        
    def prevPushButtonPressed(self):

        if not self.pagination:
            self.page_number = 1
            self.pagination = self.resPartnerController.page(self.row_number,self.page_number)
        else:
            if self.pagination.has_previous():
                self.pagination = self.resPartnerController.page(self.row_number,self.page_number - 1)
        
        
        self.customers = self.pagination.object_list
        self.page_number = self.pagination.number
        self.clear_customer_grid()
        self.fillCustomers()
    
    def nextPushButtonPressed(self):
        if not self.pagination:
            self.page_number = 0
            self.pagination = self.resPartnerController.page(self.row_number,self.page_number)
        else:
            if self.pagination.has_next():
                self.pagination = self.resPartnerController.page(self.row_number,self.page_number + 1)
        
        self.customers = self.pagination.object_list
        self.page_number = self.pagination.number
        self.clear_customer_grid()
        self.fillCustomers()

    def exitPushButtonPressed(self):
        self.controller.unload_pos_customer()

    #Private
    def _add_customer(self, customer, row, col):
        customerWidget = CustomerLine(customer.id)
        ui_path = os.path.join(self.controller.app_path, "ui/widget_customer.ui")
        uic.loadUi(ui_path, customerWidget)
        customerImageLabel = customerWidget.findChild(QLabel, 'CustomerImagaLabel')
        customerNamelabel = customerWidget.findChild(QLabel, 'CustomerNameLabel')
        customerEmailLabel = customerWidget.findChild(QLabel, 'CustomerEmailLabel')
        customerMobileLabel = customerWidget.findChild(QLabel, 'CustomerMobileLabel')
        customerNamelabel.setText(customer.name)
        customerEmailLabel.setText(customer.email)
        customerMobileLabel.setText(customer.mobile)
        self.customerGridLayout.addWidget(customerWidget, row, col)
        #self.customerGridLayout.setColumnStretch(col, col+1)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            #self.proceed()
            self.clear_customer_grid()
            print(self.searchCustomerLineEdit.text())
            self.customers = self.resPartnerController.getLocalFilterByName(self.searchCustomerLineEdit.text())
            print(self.customers)
            #self.fillCustomers()
            print("Enter")
           
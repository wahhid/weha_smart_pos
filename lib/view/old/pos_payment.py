from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QFont
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
from functools import partial
from . import *

class PosPaymentUi(QtWidgets.QDialog):

    def __init__(self, controller):
        super(PosPaymentUi, self).__init__()
        self.controller = controller
        self.payment_method_id = False

        #Controller
        self.posPaymentController = PosPaymentController(self.controller)
        self.posCategoryController = PosCategoryController(self.controller)
        self.posOrderController = PosOrderController(self.controller)
        self.posOrderLineController = PosOrderLineController(self.controller)

        self.initUi()
        self.loadInitData()
        self.loadPaymentMethod()
        self.loadPaymentLine()

    def initUi(self):
        ui_path = os.path.join(self.controller.app_path, "ui/pos_payment.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Payment')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        #Label
        self.totalLabel = self.findChild(QtWidgets.QLabel, 'TotalLabel')
        self.totalDueLabel = self.findChild(QtWidgets.QLabel, 'TotalDueLabel')
        #self.paymentMethodLabel = self.findChild(QtWidgets.QLabel, 'PaymentMethodLabel')

        #Scroll Area
        self.paymentScrollArea = self.findChild(QScrollArea, "PaymentScrollArea")

        #Vertical Layout
        self.paymentButtonVerticalLayout = self.findChild(QVBoxLayout, "PaymentButtonVerticalLayout")
        self.paymentButtonVerticalLayout.setAlignment(QtCore.Qt.AlignTop)

        self.paymentVerticalLayout = self.findChild(QVBoxLayout, "PaymentVerticalLayout")
        self.paymentVerticalLayout.setAlignment(QtCore.Qt.AlignTop)

        #LineEdit
        self.totalPaidLineEdit = self.findChild(QtWidgets.QLineEdit, 'TotalPaidLineEdit')

        #Button
        self.paidPushButton = self.findChild(QtWidgets.QPushButton, 'PaidButton')
        self.paidPushButton.clicked.connect(self.paidButtonPressed)
        self.cancelPushButton = self.findChild(QtWidgets.QPushButton, 'CancelButton')
        self.cancelPushButton.clicked.connect(self.cancelButtonPressed)

        
    def loadInitData(self):
        self.totalLabel.setText(str(self.posOrderLineController.getTotalByOrderId(self.controller.pos_order_id)))
        total_due = self.controller.posOrderUi.get_due()
        self.totalDueLabel.setText(str(total_due))

    def loadPaymentMethod(self):
        print(self.controller.posOrderUi.config_id)
        payment_methods = self.controller.posOrderUi.config_id['payment_methods']
        for payment_method in payment_methods:
            paymentButton = QPushButton()
            paymentButton.setStyleSheet(
                """QPushButton{
                    color: #ffffff;
                    background-color: #ffc107;
                    border-width: 1px;
                    color: rgb(96, 97, 97);
                    border-style: solid;
                    border-radius: 3;
                    padding: 3px;
                    padding-left: 5px;
                    padding-right: 5px;
                }
                QPushButton:pressed{
                    color :rgb(96, 97, 97);
                    background-color: #ffffff;
                    border-width: 1px;
                    border-color: : rgb(96, 97, 97);
                    border-style: solid;
                    border-radius: 3;
                    padding: 3px;
                    padding-left: 5px;
                    padding-right: 5px;
                }
                QPushButton:disabled{
                    color: rgb(82, 96, 117);
                    background-color: rgb(0, 0, 0);
                    border-width: 1px;
                    border-color: rgb(82, 96, 117);
                    border-style: solid;
                    border-radius: 3;
                    padding: 3px;
                    padding-left: 5px;
                    padding-right: 5px;
                }"""
            )
            paymentButton.setMinimumSize(0,60)
            paymentButton.setMaximumSize(16777215,60)
            paymentButton.setText(payment_method['name'])
            paymentButton.setFont(QFont('Futura', 22))
            paymentButton.clicked.connect(partial(self.paymentMethodButtonPressed, widget=paymentButton, data=payment_method))
            self.paymentButtonVerticalLayout.addWidget(paymentButton)

    def loadPaymentLine(self):
        pos_payments = self.posPaymentController.getByPosOrderId(self.controller.posOrderUi.pos_order.id)
        for pos_payment in pos_payments:
            payment_method_id = self.pos
            data = {
                'payment_line_id': pos_payment.id,
                'name': pos_payment.name,
                'amount': pos_payment.amount,
            } 
            self.add_payment(data)

    def paymentMethodButtonPressed(self, widget, data):
        if len(self.totalPaidLineEdit.text()) == 0:
            msg = QMessageBox.about(self, "Warning", "Tender Empty")
        else:
            amount = float(self.totalPaidLineEdit.text())
            data.update({'amount': amount})
            pos_payment = {
                'name': data['name'],
                'amount': amount,
                'pos_order_id': self.controller.posOrderUi.pos_order.id,
                'payment_method_id': int(data['id']),
                'session_id': self.controller.posOrderUi.pos_session['id'],
            }
            resultHandling = self.posPaymentController.insert(pos_payment)
            if not resultHandling.err:
                pos_payment  = resultHandling.data
                #total_due = self.controller.posOrderUi.get_due()
                #self.totalDueLabel.setText(str(total_due))
                data.update({'payment_line_id': pos_payment['id']})
                self.add_payment(data)
                self.totalPaidLineEdit.setText("")
            

    #Private
    def add_payment(self, data):
        paymentWidget = QWidget()
        ui_path = os.path.join(self.controller.app_path, "ui/widget_payment.ui")
        uic.loadUi(ui_path, paymentWidget)
        paymentMethodLabel = paymentWidget.findChild(QLabel, 'PaymentMethodLabel')
        paymentMethodLabel.setText(str(data['name']))
        paymentAmountLabel = paymentWidget.findChild(QLabel, 'PaymentAmountLabel')
        paymentAmountLabel.setText(str(data['amount']))
        deletePushButton = paymentWidget.findChild(QPushButton, 'DeletePushButton')
        deletePushButton.clicked.connect(partial(self.deletePushButtonPressed, paymentWidget, data))
        self.paymentVerticalLayout.addWidget(paymentWidget)

    def deletePushButtonPressed(self, widget, data):
        print("Delete Payment Widget")
        result = self.posPaymentController.delete(data['payment_line_id'])
        if result:
            widget.deleteLater()
            total_due = self.controller.posOrderUi.get_due()
            self.totalDueLabel.setText(str(total_due))
        else:
            msg = QMessageBox.about(self, "Warning", "Delete was error!")


    def paidButtonPressed(self):
        total_due = self.controller.posOrderUi.get_due()
    
        if total_due == 0:
            self.posOrderController.setPaid(self.controller.posOrderUi.pos_order.id)

            #Print Receipt
            self.controller.posOrderUi.printReceipt(self.controller.posOrderUi.pos_order.id)    

            #Send Data to Server
            #pos_order_json = self.posOrderController.getJson(self.controller.posOrderUi.pos_order.id)

            #Reset Pos Order
            self.controller.posOrderUi.pos_order = False
            self.controller.posOrderUi.totalLabel.setText("0.0")

            #Clear Product Line
            self.controller.posOrderUi.clear_product_line()
            
            #Hide Payment Screen
            self.controller.unload_pos_payment()
        else:
            pass


    def cancelButtonPressed(self):
        self.controller.unload_pos_payment()

    def pb_0ButtonPressed(self):
        print("Button 0 Clicked")
        if self.totalPaidLineEdit.hasFocus():
          self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "0")


    def pb_1ButtonPressed(self):
        print("Button 1 Clicked")
        if self.totalPaidLineEdit.hasFocus():
          self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "1")


    def pb_2ButtonPressed(self):
        print("Button 2 Clicked")
        if self.totalPaidLineEdit.hasFocus():
          self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "2")

    
    def pb_3ButtonPressed(self):
        print("Button 3 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "3")

      
    def pb_4ButtonPressed(self):
        print("Button 4 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "4")

    def pb_5ButtonPressed(self):
        print("Button 5 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "5")


    def pb_6ButtonPressed(self):
        print("Button 6 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "6")

      
    def pb_7ButtonPressed(self):
        print("Button 7 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "7")


    def pb_8ButtonPressed(self):
        print("Button 7 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "8")


    def pb_9ButtonPressed(self):
        print("Button 7 Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "9")


    def pb_delButtonPressed(self):
        print("Button Del Clicked")
        if self.totalPaidLineEdit.hasFocus():
            self.totalPaidLineEdit.setText(self.totalPaidLineEdit.text()[:-1])

        




      
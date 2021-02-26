from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QFont
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
from functools import partial
from lib.view import *

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
        ui_path = os.path.join(self.controller.app_path, "ui/q0008.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Payment')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setOffset(20, 30)
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)
        
        #Vertical Layout
        self.PaymentButtonVerticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.PaymentVerticalLayout.setAlignment(QtCore.Qt.AlignTop)

        #Button
        self.PaidButton.clicked.connect(self.paidButtonPressed)
        self.CancelButton.clicked.connect(self.cancelButtonPressed)
        
    def loadInitData(self):
        self.controller.posOrderUi.getOrderSummary()
        self.TotalLabel.setText(str(self.controller.posOrderUi.summary['total_order_line']))
        self.TotalDueLabel.setText(str(self.controller.posOrderUi.summary['total_order_line'] - self.controller.posOrderUi.summary['total_payment']))

    def loadPaymentMethod(self):
        print(self.controller.config_id)
        payment_methods = self.controller.config_id['pos_payment_methods']
        for payment_method in payment_methods:
            paymentButton = QPushButton()
            paymentButton.setStyleSheet(
                """QPushButton{
                    color: #ffff00;
                    background-color: #31363b;
                    border-width: 1px;
                    border-style: solid;
                    border-radius: 3;
                    padding: 3px;
                    padding-left: 5px;
                    padding-right: 5px;
                }
                QPushButton:pressed{
                    color : #31363b;
                    background-color:#ffff00;
                    border-width: 1px;
                    border-color: : #ffff00;
                    border-style: solid;
                    border-radius: 3;
                    padding: 3px;
                    padding-left: 5px;
                    padding-right: 5px;
                }"""
            )
            paymentButton.setMinimumSize(0,40)
            paymentButton.setMaximumSize(16777215,40)
            paymentButton.setText(payment_method['name'])
            paymentButton.setFont(QFont('Futura', 18))
            paymentButton.clicked.connect(partial(self.paymentMethodButtonPressed, widget=paymentButton, data=payment_method))
            self.PaymentButtonVerticalLayout.addWidget(paymentButton)

    # Load Payment Line - Done
    def loadPaymentLine(self):
        returnHandling = self.posPaymentController.getByPosOrderId(self.controller.posOrderUi.pos_order['id'])
        if not returnHandling.err:
            print("Load Payment Line")
            i = 0
            for pos_payment in returnHandling.data['result']:
                data = {
                    'payment_line_id':returnHandling.data['ids'][i],
                    'name': pos_payment['name'],
                    'amount': pos_payment['amount'],
                } 
                self.add_payment(data)
                i = i + 1
        else:
            print("Error Load Payment Line : " + returnHandling.message)

    def paymentMethodButtonPressed(self, widget, data):
        if len(self.TotalPaidLineEdit.text()) == 0:
            msg = QMessageBox.about(self, "Warning", "Tender Empty")
        else:
            amount = float(self.TotalPaidLineEdit.text())
            data.update({'amount': amount})
            pos_payment = {
                'name': data['name'],
                'amount': amount,
                'order': self.controller.posOrderUi.pos_order['id'],
                'pos_payment_method': int(data['id']),
                #'pos_payment_method': 3,
                'session_id': self.controller.pos_session['id'],
            }
            print(pos_payment)
            returnHandling = self.posPaymentController.insert(pos_payment)
            if not returnHandling.err:
                pos_payment = returnHandling.data['result']
                pos_payment['payment_line_id'] = returnHandling.data['id']
                self.add_payment(pos_payment)
                self.TotalPaidLineEdit.setText("")
            else:
                print(returnHandling.message)
            
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
        self.PaymentVerticalLayout.addWidget(paymentWidget)

    def deletePushButtonPressed(self, widget, data):
        print("Delete Payment Widget")
        print(data)
        returnHandling = self.posPaymentController.delete(data['payment_line_id'])
        if not returnHandling.err:
            widget.deleteLater()
            total_due = self.controller.posOrderUi.get_due()
            self.TotalDueLabel.setText(str(total_due))
        else:
            msg = QMessageBox.about(self, "Warning", returnHandling.message)

    def paidButtonPressed(self):
        self.controller.posOrderUi.getSummary()
        total_due = self.controller.posOrderUi.summary['total_order_line'] - self.controller.posOrderUi.summary['total_payment']
        if total_due == 0:
            returnHandling = self.posOrderController.setPaid(self.controller.posOrderUi.pos_order)
            if not returnHandling.err:
                #Print Receipt
                self.controller.posOrderUi.printReceipt(self.controller.posOrderUi.pos_order['id'])    

                #Send Data to Server
                #pos_order_json = self.posOrderController.getJson(self.controller.posOrderUi.pos_order.id)

                #Reset Pos Order
                self.controller.posOrderUi.pos_order = False
                self.controller.posOrderUi.pos_summary = False
                self.controller.posOrderUi.TotalLabel.setText("0.0")
                self.controller.posOrderUi.PaymentButton.setText("Payment")
                self.controller.posOrderUi.ProductLabel.setText("")
                self.controller.posOrderUi.PriceLabel.setText("@")
                self.controller.posOrderUi.QuantityButton.setText("0 pcs")
                self.controller.posOrderUi.LineTotalLabel.setText("Rp 0.0")

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
        if self.TotalPaidLineEdit.hasFocus():
          self.TotalPaidLineEdit.setText(self.totalPaidLineEdit.text() + "0")

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

        




      
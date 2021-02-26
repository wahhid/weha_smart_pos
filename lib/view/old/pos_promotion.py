from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
from functools import partial

#Controller
from lib.controller.pos_promotion import PosPromotion as PosPromotionController

class PosPromotionUi(QtWidgets.QDialog):

    def __init__(self, controller):
        super(PosPromotionUi, self).__init__()
        self.controller = controller
        self.customer_id = False

        #Controller
        self.posPromotionController = PosPromotionController(self.controller)

        self.initUi()
        self.fillPromotion()

    def initUi(self):
        ui_path = os.path.join(self.controller.app_path, "ui/pos_promotion.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle('Promotions')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)


        #Scroll Area
        self.promotionScrollArea = self.findChild(QScrollArea, "PromotionScrollArea")

        #Vertical Layout
        self.promotionVerticalLayout = self.findChild(QVBoxLayout, "PromotionVerticalLayout")
        self.promotionVerticalLayout.setAlignment(QtCore.Qt.AlignTop)

        #Button
        self.exitPushButton.clicked.connect(self.exitPushButtonPressed)

    def exitPushButtonPressed(self):
        self.controller.unload_pos_promotion()

    def fillPromotion(self):
        promotions = self.posPromotionController.getList(False)
        for promotion in promotions:
            print(promotion)
            self.add_promotion(promotion)
        
       
    #Private
    def add_promotion(self, data):
        promotionWidget = QWidget()
        ui_path = os.path.join(self.controller.app_path, "ui/widget_promo.ui")
        #ui_path = "../../ui/widget_product.ui"
        uic.loadUi(ui_path, promotionWidget)
        promotionNameLabel = promotionWidget.findChild(QLabel, 'PromotionNameLabel')
        promotionNameLabel.setText(str(data['name']))
        self.promotionVerticalLayout.addWidget(promotionWidget)

    
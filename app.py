from PyQt5 import QtWidgets, QtCore, uic
#from PyQt5.QtGui import QIcon, QPixmap
from lib.view.pos_order import PosOrderUi

import sys
import os
import qdarkstyle



#styleFile=os.path.join(os.path.split(__file__)[0],"darkorange.stylesheet")
app = QtWidgets.QApplication(sys.argv)
app_path = os.path.dirname(os.path.abspath(__file__))
#styleFile="darkorange.stylesheet"
#styleFile= app_path + "/" + "darkorange.stylesheet"
sshFile="weha.stylesheet"
#with open(sshFile,"r") as fh:
#    app.setStyleSheet(fh.read())
#app.setStyleSheet(qdarkstyle.load_stylesheet())
#app.setStyleSheet(styleSheetStr)
orderUi = PosOrderUi(app_path)
orderUi.show()
app.exec_()

class Controller(QtWidgets.QApplication):

    def __init__(self):
        super(Controller, self).__init__()

    def load_login(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    app_path = os.path.dirname(os.path.abspath(__file__))
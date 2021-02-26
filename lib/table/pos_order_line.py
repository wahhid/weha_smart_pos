from PyQt5 import QtWidgets, QtCore,  uic


class PosOrderLineTableModel(QtCore.QAbstractTableModel):
    """Model class that drives the population of tabular display"""
    def __init__(self):
        super(PosOrderLineTableModel,self).__init__()
        self.headers = ['No', 'Product Name', 'Price', 'Qty', 'Disc', 'Total']
        self.orderlines = []
 
    def rowCount(self,index=QtCore.QModelIndex()):
        return len(self.orderlines)
 
    def addPosOrderLine(self,order_line):
        self.beginResetModel()
        self.orderlines.append(order_line)
        self.endResetModel()
 
    def columnCount(self,index=QtCore.QModelIndex()):
        return len(self.headers)
 
    def data(self,index,role=QtCore.Qt.DisplayRole):
        col = index.column()
        orderline = self.orderlines[index.row()]
        #if role == Qt.DisplayRole:
        #    if col == 0:
        #        return QtCore.QVariant(person.name)
        #    elif col == 1:
        #        return QtCore.QVariant(person.city)
        #    return QtCore.QVariant()
 
    def headerData(self,section,orientation,role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
 
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant(int(section + 1))
 
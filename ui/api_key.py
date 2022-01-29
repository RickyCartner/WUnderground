from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout\
    , QCheckBox, QLineEdit, QPushButton, QTableWidget, QSpacerItem, QWidget, QHeaderView
from PyQt5 import uic
import sys


# class TableWidget(QTableWidget):
#     def mouseDoubleClickEvent(self, event):
#         ApiUi.btnDelete.setEnabled(True)
#         ApiUi.btnUpdate.setEnabled(True)

class ApiUi(QWidget):
    def __init__(self):
        super(ApiUi, self).__init__()

        uic.loadUi("api_key.ui", self)

        # Define the widgets
        self.tblAPI = self.findChild(QTableWidget, "tblAPI")
        self.btnAdd = self.findChild(QPushButton, "btnAdd")
        self.btnDelete = self.findChild(QPushButton, "btnDelete")
        self.btnUpdate = self.findChild(QPushButton, "btnUpdate")
        self.textEdit = self.findChild(QLineEdit, "textEdit")
        self.checkActive = self.findChild(QCheckBox, "checkBoxActive")



        # Functions
        self.tblAPI.doubleClicked.connect(lambda x: self.activate_fields())
        # self.btnAdd.clicked.connect()

        self.configure_widgets()

        self.show()

    def configure_widgets(self):
        # tableHeader = self.table.horizontalHeader()
        # tableHeader.setSectionResizeMode(0, QHeaderView.Stretch)
        self.tblAPI.setColumnWidth(0, 400)

    def activate_fields(self, lineItem):
        self.textEdit.setEnabled(True)
        self.textEdit.setText(lineItem)
        self.checkActive.setEnabled(True)
        self.btnDelete.setEnabled(True)
        self.btnUpdate.setEnabled(True)




app = QApplication(sys.argv)
UIWindow = ApiUi()
app.exec_()
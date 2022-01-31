from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout\
    , QCheckBox, QLineEdit, QPushButton, QTableWidget, QLabel, QWidget, QHeaderView
from PyQt5 import uic, QtCore
import sys
import os
import database
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from model import ApiModel
# from WUnderground.model import ApiModel
# from ..\model import ApiModel #, SummaryModel, MonthlyModel


class ApiUi(QWidget):
    def __init__(self):
        super(ApiUi, self).__init__()

        uic.loadUi("api_key_model.ui", self)

        # Define the widgets
        self.tblAPI = self.findChild(QTableWidget, "tblAPI")
        self.btnAdd = self.findChild(QPushButton, "btnAdd")
        self.btnDelete = self.findChild(QPushButton, "btnDelete")
        self.btnUpdate = self.findChild(QPushButton, "btnUpdate")
        self.textEdit = self.findChild(QLineEdit, "textEdit")
        self.checkActive = self.findChild(QCheckBox, "checkBoxActive")
        self.labelStatus = self.findChild(QLabel, "labelStatus")



        # Functions
        # self.api_keys = DBReadAPI().get_keys()
        # self.tblAPI.doubleClicked.connect(self.populate_selection_value)
        # self.tblAPI.clicked.connect(self.activate_fields)
        #
        # self.btnAdd.clicked.connect(self.add_api_key)
        # self.btnDelete.clicked.connect(self.delete_api_key)

        self.labelStatus.setVisible(False)

        # self.configure_table_widget()
        # self.dailyModel = ApiModel('KSCBLUFF14', '2021-02-15')
        self.dailyModel = ApiModel()

        self.show()

    def configure_table_widget(self):
        self.api_keys = DBReadAPI().get_keys()

        # Set column widths
        self.tblAPI.setColumnWidth(0, 275)
        self.tblAPI.setColumnWidth(1, 75)
        self.tblAPI.setColumnWidth(1, 100)

        row = 0
        self.tblAPI.setRowCount(len(self.api_keys))

        # Insert values and center middle column
        for api in self.api_keys:
            self.tblAPI.setItem(row, 0, QtWidgets.QTableWidgetItem(api[0]))
            # item = QtWidgets.QTableWidgetItem(str(api[1]))
            # item.setTextAlignment(QtCore.Qt.AlignHCenter)
            # self.tblAPI.setItem(row, 1, item)


            item = QtWidgets.QTableWidgetItem(str(api[1]))
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.tblAPI.setItem(row, 1, item)
            self.tblAPI.setItem(row, 2, QtWidgets.QTableWidgetItem(api[2]))
            row += 1

        # TODO: sortItems is messing up the last column
        self.tblAPI.setSortingEnabled(True)
        self.tblAPI.sortItems(1, QtCore.Qt.DescendingOrder)

    def populate_selection_value(self, index):
        self.textEdit.setText(self.tblAPI.item(index.row(), 0).text())

    def activate_fields(self):
        # self.textEdit.setEnabled(True)
        # self.checkActive.setEnabled(True)
        self.btnDelete.setEnabled(True)
        self.btnUpdate.setEnabled(True)

    def add_api_key(self):
        # TODO: add check to ensure a value exists
        text_value = self.textEdit.text()
        # self.ch = self.checkActive.isChecked()
        status = DBReadAPI().add_api(text_value, self.checkActive.isChecked())
        if status == 'success':
            self.textEdit.clear()
            self.checkActive.setChecked(False)
            self.tblAPI.sortItems(1, QtCore.Qt.DescendingOrder)

        self.configure_table_widget()
        self.labelStatus.setVisible(True)
        self.labelStatus.setText(status)

    def delete_api_key(self):
        self.textEdit.clear()
        api_key = self.tblAPI.item(self.tblAPI.currentRow(), 0).text()
        status = DBReadAPI().delete_api(api_key)
        # if not status == 'success':
        # self.api_keys.clear()
        self.configure_table_widget()
        # self.labelStatus.setVisible(True)
        # self.labelStatus.setText(status)


class DBReadAPI:
    def __init__(self):
        self.db = database.DB('..//database//weather.db')
        self.api_key_list = []

    def get_keys(self):
        self.api_key_list = self.db.fetch_all_api_keys()
        self.db.close()

        return self.api_key_list

    def update_api(self):
        pass

    def delete_api(self, api_key):
        status = self.db.delete_api_key(api_key)
        self.db.close()
        return status

    def add_api(self, api_key, active):
        status = self.db.add_api_key(api_key, active)
        self.db.close()
        return status


app = QApplication(sys.argv)
UIWindow = ApiUi()
app.exec_()
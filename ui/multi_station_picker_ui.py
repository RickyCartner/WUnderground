# -*- coding: utf-8 -*-

# Standard library imports
from datetime import date, timedelta

# Third party imports
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox
    # QApplication, QWidget, QMainWindow, QListWidget\
    # , QLabel, QDateEdit, QPushButton, QProgressBar, QTextEdit,
from PyQt5 import uic, QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QDate, QDateTime

# Local imports
from wunderground.database import DB, populate_location_cbo
from wunderground.api import history_day
from wunderground.model import MonthlyModel


class UIStationPicker(object):
    def setup_ui(self, SecondWindow, MainWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(433, 409)

        font = QtGui.QFont()
        font.setPointSize(9)

        self.labelFrom = QtWidgets.QLabel(SecondWindow)
        self.labelFrom.setGeometry(QtCore.QRect(30, 10, 81, 16))

        self.labelFrom.setFont(font)
        self.labelFrom.setObjectName("labelFrom")
        self.dateTo = QtWidgets.QDateEdit(SecondWindow)
        self.dateTo.setGeometry(QtCore.QRect(279, 30, 121, 23))
        self.dateTo.setMinimumDate(QtCore.QDate(2015, 1, 1))
        self.dateTo.setCalendarPopup(True)
        self.dateTo.setObjectName("dateTo")
        self.dateTo.setFont(font)

        self.labelTo = QtWidgets.QLabel(SecondWindow)
        self.labelTo.setGeometry(QtCore.QRect(280, 10, 81, 20))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        self.labelTo.setFont(font)
        self.labelTo.setObjectName("labelTo")
        self.dateFrom = QtWidgets.QDateEdit(SecondWindow)
        self.dateFrom.setGeometry(QtCore.QRect(30, 30, 121, 23))
        self.dateFrom.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2015, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateFrom.setMinimumDate(QtCore.QDate(2015, 1, 1))
        self.dateFrom.setCurrentSection(QtWidgets.QDateTimeEdit.MonthSection)
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setCurrentSectionIndex(0)
        self.dateFrom.setObjectName("dateFrom")
        self.dateFrom.setFont(font)

        self.btnSearch = QtWidgets.QPushButton(SecondWindow)
        self.btnSearch.setGeometry(QtCore.QRect(30, 330, 171, 31))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        self.btnSearch.setFont(font)
        self.btnSearch.setObjectName("btnSearch")
        self.btnCancel = QtWidgets.QPushButton(SecondWindow)
        self.btnCancel.setGeometry(QtCore.QRect(230, 330, 171, 31))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        self.btnCancel.setFont(font)
        self.btnCancel.setObjectName("btnCancel")
        self.listStationMainList = QtWidgets.QListWidget(SecondWindow)
        self.listStationMainList.setGeometry(QtCore.QRect(30, 70, 121, 192))
        self.listStationMainList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listStationMainList.setObjectName("listStationMainList")
        self.listStationSearch = QtWidgets.QListWidget(SecondWindow)
        self.listStationSearch.setGeometry(QtCore.QRect(280, 70, 121, 192))
        self.listStationSearch.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listStationSearch.setObjectName("listStationSearch")

        self.progressBar = QtWidgets.QProgressBar(SecondWindow)
        self.progressBar.setVisible(False)
        self.progressBar.setEnabled(False)
        self.progressBar.setGeometry(QtCore.QRect(30, 300, 371, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")

        self.btnAdd = QtWidgets.QPushButton(SecondWindow)
        self.btnAdd.setGeometry(QtCore.QRect(160, 110, 111, 25))
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.setFont(font)

        self.btnRemove = QtWidgets.QPushButton(SecondWindow)
        self.btnRemove.setGeometry(QtCore.QRect(160, 180, 111, 25))
        self.btnRemove.setObjectName("btnRemove")
        self.btnRemove.setFont(font)

        self.btnAddAll = QtWidgets.QPushButton(SecondWindow)
        self.btnAddAll.setGeometry(QtCore.QRect(160, 140, 111, 25))
        self.btnAddAll.setObjectName("btnAddAll")
        self.btnAddAll.setFont(font)

        self.btnRemoveAll = QtWidgets.QPushButton(SecondWindow)
        self.btnRemoveAll.setGeometry(QtCore.QRect(160, 210, 111, 25))
        self.btnRemoveAll.setObjectName("btnRemoveAll")
        self.btnRemoveAll.setFont(font)

        self.labelSearchStatus = QtWidgets.QLabel(SecondWindow)
        self.labelSearchStatus.setGeometry(QtCore.QRect(30, 280, 121, 16))
        self.labelSearchStatus.setObjectName("labelSearchStatus")

        self.retranslateUi(SecondWindow)
        self.btnCancel.clicked.connect(SecondWindow.close)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)
        SecondWindow.setTabOrder(self.dateFrom, self.dateTo)
        SecondWindow.setTabOrder(self.dateTo, self.listStationMainList)
        SecondWindow.setTabOrder(self.listStationMainList, self.listStationSearch)
        SecondWindow.setTabOrder(self.listStationSearch, self.btnAdd)
        SecondWindow.setTabOrder(self.btnAdd, self.btnAddAll)
        SecondWindow.setTabOrder(self.btnAddAll, self.btnRemove)
        SecondWindow.setTabOrder(self.btnRemove, self.btnRemoveAll)
        SecondWindow.setTabOrder(self.btnRemoveAll, self.btnSearch)
        SecondWindow.setTabOrder(self.btnSearch, self.btnCancel)


        self.load_stations()

        # set the date pickers to the current date and prevent future date availability
        self.dateFrom.setDate(date.today() - timedelta(days=1))
        self.dateFrom.setMaximumDate(date.today() - timedelta(days=1))
        self.dateTo.setDate(date.today() - timedelta(days=1))
        self.dateTo.setMaximumDate(date.today() - timedelta(days=1))

        # self.dateFrom.dateChanged.connect(self.date_changed)
        # self.dateTo.dateChanged.connect(self.date_changed)
        self.btnSearch.clicked.connect(lambda: self.search_clicked(MainWindow))
        self.btnAdd.clicked.connect(self.add_station)
        self.btnAddAll.clicked.connect(lambda x: self.add_station(True))
        self.btnRemove.clicked.connect(self.remove_station)
        self.btnRemoveAll.clicked.connect(lambda x: self.remove_station(True))

        self.listStationMainList.itemChanged.connect(self.sort_list)
        self.listStationSearch.itemChanged.connect(self.sort_list)

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "Multiple Station Selector"))
        self.labelFrom.setText(_translate("SecondWindow", "From Date"))
        self.labelTo.setText(_translate("SecondWindow", "To Date"))
        self.btnSearch.setText(_translate("SecondWindow", "Search"))
        self.btnCancel.setText(_translate("SecondWindow", "Cancel"))
        self.btnAdd.setText(_translate("SecondWindow", "Add >"))
        self.btnRemove.setText(_translate("SecondWindow", "< Remove"))
        self.labelSearchStatus.setText(_translate("SecondWindow", "Search Status"))
        self.btnAddAll.setText(_translate("SecondWindow", "Add All >>"))
        self.btnRemoveAll.setText(_translate("SecondWindow", "<< Remove All"))

    def search_clicked(self, main_window):
        f_date = self.dateFrom.dateTime()
        t_date = self.dateTo.dateTime()

        # used to send to api call
        from_date = f_date.toString('yyyyMMdd')
        to_date = t_date.toString('yyyyMMdd')

        if f_date > t_date:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText("From Date cannot be prior to To Date")
            msgbox.setWindowTitle("Error")
            msgbox.setStandardButtons(QMessageBox.Ok)
            return msgbox.exec_()

        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)

        # TODO: Need to add another thread for this.

        # Get the list of items to select data
        item_list = [self.listStationSearch.item(i).text() for i in range(self.listStationSearch.count())]

        # Connect to the database, return a list of active stations, close the connection
        db = DB()
        # Reset temp table for new population
        db.delete_records_from_location_temp()


        for count, item in enumerate(item_list):
            # print(count, item)

            # download the station data
            history_day(item, from_date, to_date)

            # temporarily add station ID to temp table
            db.add_record_to_location_temp(item)


            # update progress bar
            row_progress = int(count + 1 / self.listStationSearch.count()) * 100

        db.close()

        # Call the model to populate the table module
        if self.listStationSearch.count() > 1:
            multi_station_count = True
        else:
            multi_station_count = False

        # Create string from list for use in query
        station_list_string = ""
        # for item in item_list:
        #     station_list_string += f"{item}', '"
        #
        # station_list_string = station_list_string.rstrip(", '")

        station_list_temp = ', '.join([str(elem) for elem in item_list])


        self.monthly_model = MonthlyModel(station_list_temp, from_date, to_date, multi_station_count)

        # Create the table view widget
        main_window.tableViewMonthly.setModel(self.monthly_model.model)
        main_window.tableViewMonthly.setSelectionBehavior(QAbstractItemView.SelectRows)
        main_window.tableViewMonthly.resizeColumnsToContents()

    def load_stations(self):
        # Connect to the database, return a list of active stations, close the connection
        station_list = populate_location_cbo()

        self.listStationMainList.addItems(station_list)
        self.listStationMainList.setSortingEnabled(True)
        self.listStationMainList.sortItems()
        self.listStationSearch.setSortingEnabled(True)

    def sort_list(self):
        self.listStationMainList.sortItems()
        self.listStationSearch.sortItems()

    # def date_changed(self, qDate):
    #     # print(f'{qDate.month()}/{qDate.day()}/{qDate.year()}')
    #     self.textDateCheck.clear()

    def add_station(self, all_stations=False):
        """
        Add stations from left column to the right column
        """
        if not all_stations:
            # Add one station at a time to the right column
            row = self.listStationMainList.currentRow()
            row_item = self.listStationMainList.takeItem(row)
            self.listStationSearch.addItem(row_item)
        else:
            # Transfer all of the stations to the right column
            row_count = self.listStationMainList.count()
            for i in range(row_count):

                row_item = self.listStationMainList.takeItem(0)
                # item_name = self.listWidgetLeft.item(i).text()
                self.listStationSearch.addItem(row_item)

    def remove_station(self, all_stations=False):
        """
        Remove stations from right column to the left column
        """
        if not all_stations:
            # Remove one station at a time from the right column
            row = self.listStationSearch.currentRow()
            row_item = self.listStationSearch.takeItem(row)
            self.listStationMainList.addItem(row_item)
        else:
            # Remove all of the stations from the right column
            row_count = self.listStationSearch.count()
            for i in range(row_count):
                row_item = self.listStationSearch.takeItem(0)
                # item_name = self.listWidgetLeft.item(i).text()
                self.listStationMainList.addItem(row_item)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QWidget()
    ui = UIStationPicker()
    ui.setup_ui(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())

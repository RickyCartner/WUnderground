import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidget\
    , QLabel, QDateEdit, QPushButton, QProgressBar, QTextEdit
from PyQt5 import uic, Qt
from PyQt5.QtCore import QDate, QDateTime
from datetime import date


class UIDatePicker(QMainWindow):

    def __init__(self):
        super(UIDatePicker, self).__init__()

        # Load the ui file
        uic.loadUi("date_picker.ui", self)

        # Define our Widgets
        self.labelFrom = self.findChild(QLabel, "labelFrom")
        self.labelTo = self.findChild(QLabel, "labelTo")
        self.dateFrom = self.findChild(QDateEdit, "dateFrom")
        self.dateTo = self.findChild(QDateEdit, "dateTo")
        self.buttonSearch = self.findChild(QPushButton, "btnSearch")
        self.buttonCancel = self.findChild(QPushButton, "btnCancel")
        self.btnAdd = self.findChild(QPushButton, "btnAdd")
        self.btnAddAll = self.findChild(QPushButton, "btnAddAll")
        self.btnRemove = self.findChild(QPushButton, "btnRemove")
        self.btnRemoveAll = self.findChild(QPushButton, "btnRemoveAll")

        self.textDateCheck = self.findChild(QTextEdit, "textDateCheck")
        self.listWidgetLeft = self.findChild(QListWidget, "listStationMainList")
        self.listWidgetRight = self.findChild(QListWidget, "listStationSearch")

        # add stations to the left side list
        self.load_stations()
        # self.listStationMainList
        # self.listWidget = QListWidget()
        # self.listWidget.item()
        # self.listWidget.takeItem(self.listWidget.currentItem())
        # self.listWidget.selectAll()
        # self.listWidget.count()
        #
        # self.listWidget.sortItems(order='AscendingOrder')

        # Do something
        # set the date pickers to the current date and prevent future date availability
        self.dateFrom.setDateTime(QDateTime.currentDateTime())
        self.dateFrom.setMaximumDateTime(QDateTime.currentDateTime())
        self.dateTo.setDateTime(QDateTime.currentDateTime())
        self.dateTo.setMaximumDateTime(QDateTime.currentDateTime())

        self.dateFrom.dateChanged.connect(self.date_changed)
        self.dateTo.dateChanged.connect(self.date_changed)
        self.buttonSearch.clicked.connect(self.clicker)
        self.btnAdd.clicked.connect(self.add_station)
        self.btnAddAll.clicked.connect(lambda x: self.add_station(True))
        self.btnRemove.clicked.connect(self.remove_station)
        self.btnRemoveAll.clicked.connect(lambda x: self.remove_station(True))

        self.listWidgetLeft.itemChanged.connect(self.sort_list)
        self.listWidgetRight.itemChanged.connect(self.sort_list)

        # Show the app
        self.show()

    def clicker(self):
        f_date = self.dateFrom.dateTime()
        t_date = self.dateTo.dateTime()

        if f_date > t_date:
            self.textDateCheck.setPlainText(f'From Date cannot be prior to To Date')

        # self.textDateCheck.setPlainText(f'{qDate.month()}/{qDate.day()}/{qDate.year()}')
        pass

    def sort_list(self):
        self.listWidgetLeft.sortItems()
        self.listWidgetRight.sortItems()

    def date_changed(self, qDate):
        # print(f'{qDate.month()}/{qDate.day()}/{qDate.year()}')
        self.textDateCheck.clear()
        # self.textDateCheck.setPlainText(f'{qDate.month()}/{qDate.day()}/{qDate.year()}')

    def load_stations(self):
        station_list = ['KSCBEAUF36', 'KSCBEAUF78', 'KSCBEAUF100', 'KSCBEAUF13', 'KSCBEAUF40', 'KSCBEAUF105'
                        , 'KSCLADYS3', 'KSCBEAUF39', 'KSCBEAUF119', 'KSCBEAUF45', 'KSCBEAUF117'
                        , 'KSCBEAUF46', 'KSCBEAUF97']
        # station_list.sort(reverse=True)
        self.listWidgetLeft.addItems(station_list)
        self.listWidgetLeft.setSortingEnabled(True)
        self.listWidgetLeft.sortItems()
        self.listWidgetRight.setSortingEnabled(True)

    def add_station(self, all_stations=False):
        if not all_stations:
            row = self.listWidgetLeft.currentRow()
            row_item = self.listWidgetLeft.takeItem(row)
            self.listWidgetRight.addItem(row_item)
        else:
            row_count = self.listWidgetLeft.count()
            for i in range(row_count):
                row_item = self.listWidgetLeft.takeItem(i)
                # item_name = self.listWidgetLeft.item(i).text()
                self.listWidgetRight.addItem(row_item)


        # station_list.sort(reverse=True)

    def remove_station(self, all_stations=False):
        if not all_stations:
            row = self.listWidgetRight.currentRow()
            row_item = self.listWidgetRight.takeItem(row)
            self.listWidgetLeft.addItem(row_item)
        else:
            row_count = self.listWidgetRight.count()
            for i in range(row_count):
                row_item = self.listWidgetRight.takeItem(i)
                # item_name = self.listWidgetLeft.item(i).text()
                self.listWidgetLeft.addItem(row_item)


app = QApplication(sys.argv)
UIWindow = UIDatePicker()
sys.exit(app.exec_())

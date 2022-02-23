import sys
from datetime import date, timedelta
from time import sleep

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QListWidget\
    , QLabel, QDateEdit, QPushButton, QProgressBar, QTextEdit
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QDateTime

# Local
from wunderground.database import DB
from wunderground.api import history_day


class UIStationPicker(QMainWindow):

    def __init__(self, ):
        super(UIStationPicker, self).__init__()

        # Load the ui file
        uic.loadUi("ui\\multi_station_picker.ui", self)

        self.setup_ui()

    def setup_ui(self):
        # Define the Widgets
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
        self.progressBar = self.findChild(QProgressBar, "progressBar")

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

        # set the date pickers to the current date and prevent future date availability
        self.dateFrom.setDate(date.today() - timedelta(days=1))
        self.dateFrom.setMaximumDate(date.today() - timedelta(days=1))
        self.dateTo.setDate(date.today() - timedelta(days=1))
        self.dateTo.setMaximumDate(date.today() - timedelta(days=1))
        # self.dateFrom.setDateTime(date.today() - timedelta(days=1))
        # self.dateFrom.setMaximumDateTime(date.today() - timedelta(days=1))
        # self.dateTo.setDateTime(date.today() - timedelta(days=1))
        # self.dateTo.setMaximumDateTime(date.today() - timedelta(days=1))
        # self.dateTo.setMaximumDateTime(QDateTime.currentDateTime())

        self.dateFrom.dateChanged.connect(self.date_changed)
        self.dateTo.dateChanged.connect(self.date_changed)
        self.buttonSearch.clicked.connect(self.search_clicked)
        self.btnAdd.clicked.connect(self.add_station)
        self.btnAddAll.clicked.connect(lambda x: self.add_station(True))
        self.btnRemove.clicked.connect(self.remove_station)
        self.btnRemoveAll.clicked.connect(lambda x: self.remove_station(True))

        self.listWidgetLeft.itemChanged.connect(self.sort_list)
        self.listWidgetRight.itemChanged.connect(self.sort_list)

        # Show the app
        self.show()

    def search_clicked(self):
        self.main_window = Window()

        f_date = self.dateFrom.dateTime()
        t_date = self.dateTo.dateTime()

        # used to send to api call
        from_date = f_date.toString('yyyyMMdd')
        to_date = t_date.toString('yyyyMMdd')

        if f_date > t_date:
            self.textDateCheck.setPlainText(f'From Date cannot be prior to To Date')
            return

        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)

        # TODO: Need to add another thread for this.

        # Get the list of items to select data
        item_list = [self.listWidgetRight.item(i).text() for i in range(self.listWidgetRight.count())]

        for count, item in enumerate(item_list):
            # print(count, item)
            history_day(item, from_date, to_date)

            # update progress bar
            row_progress = int(count + 1 / self.listWidgetRight.count()) * 100
            self.main_window.label_info_station_id.setText("Hello Ricky")



        # row_count = self.listWidgetRight.count()
        # for i in range(row_count):
        #     row_item = self.listWidgetLeft
        #     # item_name = self.listWidgetLeft.item(i).text()
        #     self.listWidgetRight.addItem(row_item)
        #
        # for i in range(row_count):
        #     # update progress bar
        #     row_progress = int(i+1 / row_count) * 100
        #     self.progressBar.setValue(50)
        #     # sleep(1)
        #
        #     weather_station = self.listWidgetRight.item(i)
        #
        #     # Use api.py, history_day function
        #     history_day(weather_station, from_date, to_date)

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
        # Connect to the database, return a list of active stations, close the connection
        db = DB()
        station_list = db.populate_location_cbo()
        db.close()

        # station_list = ['KSCBEAUF36', 'KSCBEAUF78', 'KSCBEAUF100', 'KSCBEAUF13', 'KSCBEAUF40', 'KSCBEAUF105'
        #                 , 'KSCLADYS3', 'KSCBEAUF39', 'KSCBEAUF119', 'KSCBEAUF45', 'KSCBEAUF117'
        #                 , 'KSCBEAUF46', 'KSCBEAUF97']
        # station_list.sort(reverse=True)
        self.listWidgetLeft.addItems(station_list)
        self.listWidgetLeft.setSortingEnabled(True)
        self.listWidgetLeft.sortItems()
        self.listWidgetRight.setSortingEnabled(True)

    def add_station(self, all_stations=False):
        """
        Add stations from left column to the right column
        """
        if not all_stations:
            # Add one station at a time to the right column
            row = self.listWidgetLeft.currentRow()
            row_item = self.listWidgetLeft.takeItem(row)
            self.listWidgetRight.addItem(row_item)
        else:
            # Transfer all of the stations to the right column
            row_count = self.listWidgetLeft.count()
            for i in range(row_count):

                row_item = self.listWidgetLeft.takeItem(0)
                # item_name = self.listWidgetLeft.item(i).text()
                self.listWidgetRight.addItem(row_item)


        # station_list.sort(reverse=True)

    def remove_station(self, all_stations=False):
        """
        Remove stations from right column to the left column
        """
        if not all_stations:
            # Remove one station at a time from the right column
            row = self.listWidgetRight.currentRow()
            row_item = self.listWidgetRight.takeItem(row)
            self.listWidgetLeft.addItem(row_item)
        else:
            # Remove all of the stations from the right column
            row_count = self.listWidgetRight.count()
            for i in range(row_count):
                row_item = self.listWidgetRight.takeItem(0)
                # item_name = self.listWidgetLeft.item(i).text()
                self.listWidgetLeft.addItem(row_item)


def main():
    app = QApplication(sys.argv)
    UIWindow = UIStationPicker()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

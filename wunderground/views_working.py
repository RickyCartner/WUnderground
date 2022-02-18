# -*- coding: utf-8 -*-

"""This module provides views to manage the main window."""

from datetime import date, timedelta

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QMainWindow,
    QVBoxLayout,
    QMainWindow, QWidget,
    QTableView,
    QPushButton, QCheckBox, QLineEdit, QLabel,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox,
)

from .model import ApiModel, MonthlyModel
from .database import populate_location_cbo

from .api import history_day
from ui.main_form import Ui_WUnderground
from ui.multi_station_picker import UIStationPicker
# import .api


class Window(QMainWindow):
    """ Main Window """

    def __init__(self, parent=None):
        """ Initializer """
        super().__init__(parent)
        # self.window = QMainWindow()
        self.main_ui = Ui_WUnderground()
        self.main_ui.setupUi(self)
        # self.window.show()

        # app = QtWidgets.QApplication(sys.argv)
        # WUnderground = QtWidgets.QMainWindow()
        # ui = Ui_WUnderground()
        # ui.setupUi(WUnderground)
        # WUnderground.show()

        # uic.loadUi("ui\\main\\form.ui", self)

        self.setup_ui()

    """Setup the main window's GUI."""
    def setup_ui(self):

        # Clear the combobox and add the list of locations from the database
        self.main_ui.comboBox_WeatherStation.clear()
        self.main_ui.comboBox_WeatherStation.addItems(populate_location_cbo())

        # Set the max date and From and To dates to todays date
        self.main_ui.dateFrom.setMaximumDate(date.today() - timedelta(days=1))
        self.main_ui.dateTo.setMaximumDate(date.today() - timedelta(days=1))
        self.main_ui.dateFrom.setDate(date.today() - timedelta(days=1))
        self.main_ui.dateTo.setDate(date.today() - timedelta(days=1))

        # d = datetime.today() - timedelta(days=days_to_subtract)

        # Set the "Fetch" button click event
        self.main_ui.btnFetchData.clicked.connect(self.fetch_data)
        self.main_ui.actionMultiple_Stations.triggered.connect(self.multi_station_ui)

    def multi_station_ui(self):
        self.window = QMainWindow()
        self.multi_ui = UIStationPicker()
        self.multi_ui.setup_ui()
        self.window.show()

    '''
    Get the weather date for the weather station and date range
    and display it on the main form
    '''
    def fetch_data(self):
        # Get the From and To dates and convert them to a format the API can read
        begin_date = self.main_ui.dateFrom.date()
        begin_date = begin_date.toString('yyyyMMdd')
        end_date = self.main_ui.dateTo.date()
        end_date = end_date.toString('yyyyMMdd')

        # Get the weather station to search
        weather_station = self.main_ui.comboBox_WeatherStation.currentText()

        # Use api.py, history_day function
        history_day(weather_station, begin_date, end_date)

        # Call the model to populate the table module
        self.monthly_model = MonthlyModel(weather_station, begin_date, end_date)

        # Create the table view widget
        self.main_ui.tableViewMonthly.setModel(self.monthly_model.model)
        self.main_ui.tableViewMonthly.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.main_ui.tableViewMonthly.resizeColumnsToContents()


class ApiUi(QWidget):
    def __init__(self):
        super(ApiUi, self).__init__()

        uic.loadUi("ui\\api_key_model.ui", self)

        # Define the widgets
        self.tblAPI = self.findChild(QTableView, "tblAPI")
        self.btnAdd = self.findChild(QPushButton, "btnAdd")
        self.btnDelete = self.findChild(QPushButton, "btnDelete")
        self.btnUpdate = self.findChild(QPushButton, "btnUpdate")
        self.textEdit = self.findChild(QLineEdit, "textEdit")
        self.checkActive = self.findChild(QCheckBox, "checkBoxActive")
        self.labelStatus = self.findChild(QLabel, "labelStatus")

        self.labelStatus.setVisible(False)

        self.apiModel = ApiModel()
        self.setup_ui()

    def setup_ui(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.tblAPI.setModel(self.apiModel.model)
        self.tblAPI.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblAPI.resizeColumnsToContents()

        self.btnAdd.clicked.connect(self.open_add_dialog)

    def open_add_dialog(self):
        """Open the Add Contact dialog."""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.apiModel.addAPI(dialog.data)
            self.tblAPI.resizeColumnsToContents()


class AddDialog(QDialog):
    """ Add new API """
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add API")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.api_field = QLineEdit()
        self.active_field = QLineEdit()
        self.note_field = QLineEdit()

        self.buttonsBox = QDialogButtonBox(self)

        self.setup_ui()

    def setup_ui(self):
        """ Setup the Add API GUI """

        # Create line edits for data fields
        self.api_field.setObjectName("API")
        self.active_field.setObjectName("Active")
        self.note_field.setObjectName("Note")

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("API:", self.apiField)
        layout.addRow("Active:", self.activeField)
        layout.addRow("Note:", self.noteField)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        for field in (self.apiField, self.activeField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return

            self.data.append(field.text())

        self.data.append(self.noteField.text())

        if not self.data:
            return

        super().accept()

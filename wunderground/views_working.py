# -*- coding: utf-8 -*-

"""This module provides views to manage the main window."""

from datetime import date, timedelta, datetime

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

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
    QMessageBox
)

from .model import ApiModel, MonthlyModel
from .database import populate_location_cbo

from .api import history_day
from ui.main_form import Ui_WUnderground
from ui.multi_station_picker import UIStationPicker
# import .api


# TODO: Need to add a button to clear all of the data to reset

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

    def setup_ui(self):
        """Setup the main window's GUI."""
        # Clear the combobox and add the list of locations from the database
        self.main_ui.comboBox_WeatherStation.clear()
        self.main_ui.comboBox_WeatherStation.addItems(populate_location_cbo())

        # Set the max date and From and To dates to todays date
        self.main_ui.dateFrom.setMaximumDate(date.today() - timedelta(days=1))
        self.main_ui.dateTo.setMaximumDate(date.today() - timedelta(days=1))
        self.main_ui.dateFrom.setDate(date.today() - timedelta(days=1))
        self.main_ui.dateTo.setDate(date.today() - timedelta(days=1))

        # Clear the information detail header
        self.main_ui.label_info_station_id.setText('')
        self.main_ui.label_info_date.setText('')

        # Disable editing cells in the table view
        self.main_ui.tableViewMonthly.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set the "Fetch" button click event
        self.main_ui.btnFetchData.clicked.connect(self.fetch_data)
        self.main_ui.btnClearData.clicked.connect(self.clear_data)
        self.main_ui.actionMultiple_Stations.triggered.connect(self.multi_station_ui)

        self.main_ui.tableViewMonthly.doubleClicked.connect(self.station_details_by_date)

    def multi_station_ui(self):
        """
        Open the UI for selecting multiple stations
        """
        self.multi_ui = UIStationPicker()
        self.multi_ui.show()

    def fetch_data(self):
        """
        Get the weather date for the weather station and date range
        and display it on the main form
        """
        # Disable widgets
        self.enable_widgets(False)

        # Get the From and To dates and convert them to a format the API can read
        begin_date = self.main_ui.dateFrom.date()
        begin_date = begin_date.toString('yyyyMMdd')
        end_date = self.main_ui.dateTo.date()
        end_date = end_date.toString('yyyyMMdd')

        if begin_date > end_date:
            QMessageBox.critical(
                self,
                "Date Error",
                f"From date cannot be later than To date",
            )
            # self.textDateCheck.setPlainText(f'From Date cannot be prior to To Date')

            # Enable widgets
            self.enable_widgets(True)
            return

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

        # Enable widgets
        self.enable_widgets(True)

    def enable_widgets(self, enabled):
        # Disable widgets
        self.main_ui.btnFetchData.setEnabled(enabled)
        self.main_ui.btnClearData.setEnabled(enabled)

    def clear_data(self):
        """ Clear all of the data and settings """
        self.main_ui.tableViewMonthly.setModel(None)

        # Recreate the QTableView because it was cleared and re-add the headers
        model = QStandardItemModel()
        headers = MonthlyModel.add_model_headers()
        model.setHorizontalHeaderLabels(headers)
        self.main_ui.tableViewMonthly.setModel(model)

        # Find all QLineEdit fields; if they begin with "txt" delete the contents
        for widget in self.main_ui.centralwidget.findChildren(QLineEdit):
            if widget.objectName()[:3] == 'txt':
                widget.clear()

        # Reset date selections
        self.main_ui.dateFrom.setDate(date.today() - timedelta(days=1))
        self.main_ui.dateTo.setDate(date.today() - timedelta(days=1))

        # Clear the information detail header
        self.main_ui.label_info_station_id.setText('')
        self.main_ui.label_info_date.setText('')

    def station_details_by_date(self, item):
        items_dict = {}
        for column, idx in enumerate(self.main_ui.tableViewMonthly.selectionModel().selectedIndexes()):
            header = self.main_ui.tableViewMonthly.model().headerData(column, Qt.Horizontal)
            items_dict[header] = self.main_ui.tableViewMonthly.model().data(idx)

        record_date = datetime.strptime(items_dict.get('Record Date'), '%Y-%m-%d %H:%M:%S')
        # record_date = record_date.toString('MM/dd/yyyy')

        self.main_ui.label_info_station_id.setText(str(items_dict.get('Station ID')))
        self.main_ui.label_info_date.setText(record_date.strftime('%m/%d/%Y'))

        self.main_ui.txtTempHigh.setText(str(items_dict.get('Temp High')))
        self.main_ui.txtTempAvg.setText(str(items_dict.get('Temp Avg')))
        self.main_ui.txtTempLow.setText(str(items_dict.get('Temp Low')))

        self.main_ui.txtDewPointHigh.setText(str(items_dict.get('Dew Point High')))
        self.main_ui.txtDewPointAvg.setText(str(items_dict.get('Dew Point Avg')))
        self.main_ui.txtDewPointLow.setText(str(items_dict.get('Dew Point Low')))

        self.main_ui.txtHeatIndexHigh.setText(str(items_dict.get('Heat Index High')))
        self.main_ui.txtHeatIndexAvg.setText(str(items_dict.get('Heat Index Avg')))
        self.main_ui.txtHeatIndexLow.setText(str(items_dict.get('Heat Index Low')))

        self.main_ui.txtWindSpeedHigh.setText(str(items_dict.get('Speed High')))
        self.main_ui.txtWindSpeedAvg.setText(str(items_dict.get('Speed Avg')))
        self.main_ui.txtWindSpeedLow.setText(str(items_dict.get('Speed Low')))

        self.main_ui.txtWindGustHigh.setText(str(items_dict.get('Gust High')))
        self.main_ui.txtWindGustAvg.setText(str(items_dict.get('Gust Avg')))
        self.main_ui.txtWindGustLow.setText(str(items_dict.get('Gust Low')))

        self.main_ui.txtWindChillHigh.setText(str(items_dict.get('Chill High')))
        self.main_ui.txtWindChillAvg.setText(str(items_dict.get('Chill Avg')))
        self.main_ui.txtWindChillLow.setText(str(items_dict.get('Chill Low')))

        self.main_ui.txtPressureMax.setText(str(items_dict.get('Pressure Max')))
        self.main_ui.txtPressureMin.setText(str(items_dict.get('Pressure Min')))
        self.main_ui.txtPressureTrend.setText(str(items_dict.get('Pressure Trend')))

        self.main_ui.txtPrecipationRate.setText(str(items_dict.get('Precipitation Rate')))
        self.main_ui.txtPrecipationTotal.setText(str(items_dict.get('Precipitation Total')))


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

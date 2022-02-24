# -*- coding: utf-8 -*-

"""This module provides views to manage the main window."""

from datetime import date, timedelta, datetime

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QIcon

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
    QMessageBox, QComboBox
)

from .model import ApiModel, MonthlyModel
from .database import (
    populate_location_cbo, update_location_cbo,
    delete_location, delete_history
)

from .api import history_day
from ui.main_form import Ui_WUnderground
# from ui.multi_station_picker import UIStationPicker
from ui.multi_station_picker_ui import UIStationPicker
from wunderground.export_to_excel import open_excel
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

        self._create_actions()

    def _create_actions(self):
        # Set the "Fetch" button click event
        self.main_ui.btnFetchData.clicked.connect(self.fetch_data)
        self.main_ui.btnClearData.clicked.connect(self.clear_data)

        # File menu items
        self.main_ui.actionExport.triggered.connect(self.export_to_excel)

        # Edit menu items
        self.main_ui.actionMultiple_Stations.triggered.connect(self.multi_station_ui)
        self.main_ui.actionAPI_Key.triggered.connect(self.add_api_key)
        self.main_ui.actionAddStation.triggered.connect(self.open_add_dialog)
        self.main_ui.actionDeleteStation.triggered.connect(self.delete_location)

        # Help menu items
        self.main_ui.actionAbout.triggered.connect(self.about_me)

        self.main_ui.tableViewMonthly.doubleClicked.connect(self.station_details_by_date)

    def about_me(self):
        AboutApplication(self)

    def open_add_dialog(self):
        """Open the Add Location dialog box"""
        dialog = AddLocationDialog(self)
        dialog.setWindowIcon(QIcon("images/add-station.png"))

        # If [OK] is pressed, add the record
        if dialog.exec() == QDialog.Accepted:
            query_status = update_location_cbo(dialog.data)

            if query_status == "updated":
                QMessageBox.information(
                    self,
                    "Successful Update",
                    f"Record was successfully added",
                )
            else:
                QMessageBox.critical(
                    self,
                    "No change",
                    f"This record already exists",
                )

            self.main_ui.comboBox_WeatherStation.clear()
            self.main_ui.comboBox_WeatherStation.addItems(populate_location_cbo())

    def delete_location(self):

        # Call the function to select a location to delete and return the location as "dialog"
        dialog = DeleteLocationDialog(self)

        # Call/Return results from the delete method
        if dialog.exec_() == QDialog.Accepted:
            # Call database.py to remove weather station from database
            delete_location_status = delete_location(dialog.data)
            delete_history_status = delete_history(dialog.data)

            # Set up the message box
            msg = QMessageBox()
            msg.setWindowTitle("Delete Results")
            msg.setWindowIcon(QIcon("images/weather-station.png"))

            # If no error, reset combobox and display message, otherwise display error message
            if delete_location_status == "Delete Successful" and delete_history_status == "Delete Successful":
                self.main_ui.comboBox_WeatherStation.clear()
                self.main_ui.comboBox_WeatherStation.addItems(populate_location_cbo())

                msg.setIcon(QMessageBox.Information)
                msg.setText(dialog.data + " has been removed")

            elif delete_location_status != "Delete Successful":
                msg.setIcon(QMessageBox.Warning)
                msg.setText(delete_location_status)

            elif delete_history_status != "Delete Successful":
                msg.setIcon(QMessageBox.Warning)
                msg.setText(delete_history_status)

            msg.exec()

    def multi_station_ui(self):
        """ Open the UI for selecting multiple stations """

        self.multi_window = QMainWindow()
        self.multi_ui = UIStationPicker()
        self.multi_ui.setupUi(self.multi_window, self.main_ui)
        self.multi_window.show()

    def export_to_excel(self):
        """ Export data in table to xlsx """
        status = Exporting(self.main_ui)

    def add_api_key(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            print("Here i am")
        else:
            print("cancelled")
            # self.apiModel.addAPI(dialog.data)
            # self.tblAPI.resizeColumnsToContents()
        # self.api_window = QDialog()
        # self.api_ui = AddDialog()
        # self.api_ui.setup_ui(self.api_window)
        # self.api_window.show()

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
        # self.setWindowTitle("Add API")
        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        # self.data = None
        #
        # self.api_field = QLineEdit()
        # self.active_field = QLineEdit()
        # self.note_field = QLineEdit()
        #
        # self.buttonsBox = QDialogButtonBox(self)

        # Create line edits for data fields
        self.api_field.setObjectName("API")
        self.active_field.setObjectName("Active")
        self.note_field.setObjectName("Note")

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("API:", self.api_field)
        layout.addRow("Active:", self.active_field)
        layout.addRow("Note:", self.note_field)
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
        """
        Accept the data provided through the dialog
        The user must enter an API and select if it is active or not
        """
        self.data = []
        for field in (self.api_field, self.active_field):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return

            self.data.append(field.text())

        self.data.append(self.note_field.text())

        if not self.data:
            return

        super().accept()


class Exporting:
    """ Using the information in the Monthly Data model, export to an XLSX file """
    def __init__(self, main_window):
        mw = main_window
        self.export_to_excel(mw)

    def export_to_excel(self, main_window):

        try:
            # Get information from the Monthly Data model
            # m = self.tableM.model()
            # m = main_window.tableViewMonthly.model()
            #
            # # Find the last row
            # m_last_record = m.rowCount() - 1
            #
            # # Weather location from the last row
            # curr_location = m.data(m.index(m_last_record, 0))
            #
            # # Date from the last row
            # curr_date = m.data(m.index(m_last_record, 1))
            #
            # # Convert from a string to a date (using the format given from the model)
            # dt_curr_date = datetime.strptime(curr_date, '%Y-%m-%d').date()
            #
            # # Get the day of the last day of the month
            # int_day = dt_curr_date.day
            #
            # # Get the first day of the month by subtracting the number of days in the month from the last day in the model
            # from_date = str(dt_curr_date - timedelta(days=(int_day - 1)))
            # to_date = str(dt_curr_date)

            items_dict = {}
            items_lst = []
            model = main_window.tableViewMonthly.model()

            # Loop through each item in the table and add to a dictionary.
            for row in range(model.rowCount()):
                for column in range(model.columnCount()):
                    header = main_window.tableViewMonthly.model().headerData(column, Qt.Horizontal)
                    idx = model.index(row, column)
                    items_dict[header] = main_window.tableViewMonthly.model().data(idx)

                # Copy the dictionary and append to a list
                # The copy prevents the next loop from changing the data in the dictionary already added to the list
                dict_copy = items_dict.copy()
                items_lst.append(dict_copy)

            # Pass the list of items to export
            open_excel(items_lst)

        # Error handling
        except Exception as e:
            print(e)
            # self.display_message(2, str(e), "No Data")

        return

# ###########################################
# Special message boxes
# ###########################################


class AddLocationDialog(QDialog):
    """Add Website location"""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Location")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Remove question mark from header
        self.setWindowIcon(QIcon("images/add-station.png"))
        self.setFixedSize(250, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setup_ui()

    # Make each letter typed, a capitol letter
    def on_changed(self, text):
        self.location_field.setText(text.upper())

    def setup_ui(self):
        """Setup the Add Location dialog's GUI."""
        # Create line edits for data fields
        self.location_field = QLineEdit()
        self.location_field.setObjectName("Location")
        self.location_field.textChanged[str].connect(self.on_changed)

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Location:", self.location_field)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them
        self.buttons_box = QDialogButtonBox(self)
        self.buttons_box.setOrientation(Qt.Horizontal)
        self.buttons_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons_box)

    def accept(self):
        """Accept the data provided through the dialog."""

        if not self.location_field.text():
            QMessageBox.critical(
                self,
                "Error!",
                f"You must enter a Location",
            )
            self.data = None  # Reset .data
            return

        self.data = self.location_field.text()

        if not self.data:
            return

        super().accept()


class DeleteLocationDialog(QDialog):
    """Add Website location"""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Delete Location")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Remove question mark from header
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon("images/delete-station.png"))
        self.setFixedSize(250, 100)
        self.data = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the Delete Location dialog's GUI."""
        # Create line edits for data fields
        self.location_combobox = QComboBox(self)

        # Populate the combobox to select a location to delete
        self.location_combobox.clear()
        self.location_combobox.addItems(populate_location_cbo())

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Select Location:", self.location_combobox)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them
        self.buttons_box = QDialogButtonBox(self)
        self.buttons_box.setOrientation(Qt.Horizontal)
        self.buttons_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons_box)

    def accept(self):
        """Accept the data provided through the dialog."""

        button_reply = QMessageBox()
        button_reply.setWindowTitle("Delete All Data")
        button_reply.setText(
            "This action will remove ALL data related to this weather station\n\n"
            "Do you want to continue removing this weather station?"
        )

        button_reply.setIcon(QMessageBox.Question)
        button_reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button_reply.setDefaultButton(QMessageBox.No)
        button_reply.setWindowIcon(QIcon("images/delete-station.png"))

        # Get the results of the delete confirmation
        if button_reply.exec_() == QMessageBox.Yes:
            # If user selected OK, get the value of the location to delete
            self.data = self.location_combobox.currentText()
        else:
            self.data = None  # Reset .data
            return

        if not self.data:
            return

        super().accept()


class AboutApplication(QDialog):
    """ About the application """

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("About Me")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Remove question mark from header
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # self.setWindowIcon(QtGui.QIcon("images/delete-station.png"))
        self.setFixedSize(250, 100)
        self.data = None

        self.setupUI()

    def setupUI(self):
        """Setup the Delete Location dialog's GUI."""
        # Create line edits for data fields
        button_reply = QMessageBox()
        button_reply.setWindowTitle("About Application")
        button_reply.setText("WUnderground Weather Information Collection\n\n"
                             "Free, open-source application for collecting information\n"
                             "from weather stations whose information is managed in WUnderground.\n\n"
                             "Version: 1.0\n"
                             "Author: Ricky Cartner\n"
                             "Last Updated: 2/24/2022"
                             )

        button_reply.setIcon(QMessageBox.Information)
        button_reply.setStandardButtons(QMessageBox.Ok)
        button_reply.setDefaultButton(QMessageBox.Ok)

        button_reply.exec_()

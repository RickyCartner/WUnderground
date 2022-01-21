"""This module provides the layout and management of the main application"""

from database import *
import get_web_data
import get_list_of_websites
import export_to_excel
from model import DailyModel, SummaryModel, MonthlyModel
from PyQt5 import QtCore, QtSql, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QIcon, QPixmap
from datetime import datetime, date, timedelta


# Allows multi-threading
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(bool)

    def run(self):
        """Long-running task."""
        self.progress.emit(True)

        self.finished.emit()


class Window(QMainWindow):
    """ Main Window """
    def __init__(self, parent=None):
        """ Initializer """
        super().__init__(parent)
        self.setWindowTitle("WUnderground Weather Information Collection")
        self.setWindowIcon(QIcon("images/weather-station.png"))
        # self.resize(550, 350)
        # self.setFixedWidth(900)
        self.setMinimumWidth(900)

        # Make "centralWidget" the main container
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Set the main layout to apply widgets in a vertical fashion and apply it to the main container
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Call [model.py] to set values for display boxes
        # self.dailyModel = DailyModel('KSCBLUFF14', '2021-02-15')
        # self.summaryModel = SummaryModel('KSCBLUFF14', '2021-02-19')
        # self.monthlyModel = MonthlyModel('', '', '')

        # Setup the main window's GUI
        self._createActions()
        self._createMenuBar()
        self.setup_UI()

    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)

        # Creating actions using the second constructor
        self.importAction = QAction(QIcon("images/import.png"), "&Bulk Location Import...", self)
        self.importAction.triggered.connect(self.bulk_update)


        # Exit menu item
        self.exitAction = QAction(self.style().standardIcon(QStyle.SP_DialogCancelButton),
                             '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(qApp.quit)

        # Add Location menu item
        self.addLocation = QAction(QIcon("images/add-station.png"),
                                  "Add &Location", self)
        self.addLocation.setShortcut('Ctrl+L')
        self.addLocation.triggered.connect(self.openAddDialog)

        # Remove Location menu item
        self.removeLocation = QAction(QIcon("images/delete-station.png"),
                                   "&Delete Location", self)
        self.removeLocation.setShortcut('Ctrl+D')
        self.removeLocation.triggered.connect(self.delete_location)

        # Export to Excel menu item
        self.exportData = QAction(QIcon("images/export.png"),
                                      "&Export to Excel", self)
        self.exportData.setShortcut('Ctrl+E')
        self.exportData.triggered.connect(self.export_to_excel)
        self.exportData.setEnabled(False)

        # Help menu items
        self.aboutAction = QAction("&About", self)
        self.aboutAction.triggered.connect(self.about_me)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating Menus using a QMenu object
        file_menu = QMenu("&File", self)
        menuBar.addMenu(file_menu)
        file_menu.addAction(self.importAction)
        file_menu.addAction(self.exitAction)

        # Edit Menu
        edit_menu = menuBar.addMenu("&Edit")
        edit_menu.addAction(self.addLocation)
        edit_menu.addAction(self.removeLocation)
        edit_menu.addAction(self.exportData)

        # Help Menu
        help_menu = menuBar.addMenu("&Help")
        help_menu.addAction(self.aboutAction)

    def last_day_of_month(self, any_day):
        # get close to the end of the month for any day, and add 4 days 'over'
        next_month = any_day.replace(day=28) + timedelta(days=4)
        # subtract the number of remaining 'overage' days to get last day of current month
        return next_month - timedelta(days=next_month.day)

    def clear_all_button_pressed(self):
        self.tableD.setModel(None)
        self.tableS.setModel(None)
        self.tableM.setModel(None)
        self.exportButton.setEnabled(False)
        self.exportData.setEnabled(False)

    # Default error messages
    def display_message(self, message_type, message_text, message_header):
        if message_type == 1:
            QMessageBox.information(
                self,
                "Successful Update",
                f"Record was successfully added",
            )
        elif message_type == 2:
            QMessageBox.critical(
                self
                , message_header
                , message_text.ljust(40)
            )
        elif message_type == 3:

            QMessageBox.information(
                self
                , message_header
                , message_text.ljust(40)
            )


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
                self.location_combobox.clear()
                self.location_combobox.addItems(populate_location_cbo())

                msg.setIcon(QMessageBox.Information)
                msg.setText(dialog.data + " has been removed")

            elif delete_location_status != "Delete Successful":
                msg.setIcon(QMessageBox.Warning)
                msg.setText(delete_location_status)

            elif delete_history_status != "Delete Successful":
                msg.setIcon(QMessageBox.Warning)
                msg.setText(delete_history_status)

            msg.exec()

    def about_me(self):
        About_Application(self)

    def fetch_button_pressed(self):

        # Display loading message
        self.loading.setVisible(True)

        # #############################################################
        # Creating multi-thread process
        # This is needed for the "loading message" to be displayed
        # #############################################################
        # Create a QThread object
        self.thread = QThread()
        # Create a worker object
        self.worker = Worker()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.get_record_data)
        # Start the thread
        self.thread.start()


    def get_record_data(self):

        if self.location_combobox.currentText() != "":
            # print(self.dateedit.date().toPyDate())
            # print(self.location_combobox.currentText())
            int_day = self.dateedit.date().day()
            int_month = self.dateedit.date().month()
            int_year = self.dateedit.date().year()

            if self.dateedit.date() > datetime.now():
                self.loading.setVisible(False)
                self.display_message(2, "You must select a date prior to today", "Fetch Status")
                return

            # ##########################
            # Check if records exist
            # ##########################
            record_count = fetch_records(self.location_combobox.currentText()
                                         , str(self.dateedit.date().toPyDate()), "tbl_history")
            # If no records exist, pull data from the web and update the database
            if record_count == 0:
                from_date = str(self.dateedit.date().toPyDate() - timedelta(days=(int_day - 1)))
                to_date = str(self.dateedit.date().toPyDate())
                return_value = get_web_data.get_web_data(self.location_combobox.currentText().split(), from_date,
                                                         to_date, "monthly")
            else:
                return_value = ""

            # If web data was found, populate the screen, otherwise display an error message
            # if return_value != "No web data available" and return_value != "No web data available - Station is Offline":
            if return_value[0:21] != "No web data available":

                # ##########################
                # Update Daily table data
                # ##########################
                self.dailyModel = DailyModel(self.location_combobox.currentText(), str(self.dateedit.date().toPyDate()))
                # self.dailyModel = DailyModel('KSCBLUFF14', '2021-02-15')
                self.tableD.setModel(self.dailyModel.model)
                self.tableD.setFixedHeight(79)

                # self.tableD.horizontalHeader().setStyleSheet("background-color: #99ccff;")

                # self.tableD.verticalHeader().setStyleSheet("color: #99ccff;")

                self.tableD.resizeColumnsToContents()
                for c in range(0, 14):
                    self.tableD.setColumnWidth(c, self.tableD.columnWidth(c) + 10)
                self.tableD.horizontalHeader().setStyleSheet("QHeaderView.section {background-color: #DCDCDC; font-size: 20px;}")


                # ##########################
                # Update Summary table data
                # ##########################
                # Query database and populate GUI
                begin_date = str(date(int_year, int_month, 1))
                end_date = str(self.dateedit.date().toPyDate())

                self.summaryModel = SummaryModel(self.location_combobox.currentText(), begin_date, end_date)
                self.tableS.setModel(self.summaryModel.model)
                self.tableS.setFixedHeight(79)
                self.tableS.resizeColumnsToContents()
                for c in range(0, 14):
                    self.tableS.setColumnWidth(c, self.tableS.columnWidth(c) + 10)


                self.summary_data_label = QLabel('Month-to-date Average', self)

                # ##########################
                # Update Monthly table data
                # ##########################

                begin_date = str(date(int_year, int_month, 1))
                end_date = str(self.last_day_of_month(date(int_year, int_month, 1)))

                self.monthlyModel = MonthlyModel(self.location_combobox.currentText(), begin_date, end_date)
                self.tableM.setModel(self.monthlyModel.model)
                self.tableM.setAlternatingRowColors(True)
                self.tableM.setStyleSheet("alternate-background-color: #E8E8E8;")
                self.tableM.resizeColumnsToContents()
                for c in range(0, 14):
                    self.tableM.setColumnWidth(c, self.tableM.columnWidth(c) + 10)

                # Enable Export button
                self.exportButton.setEnabled(True)
                self.exportData.setEnabled(True)

                # Display result status
                self.loading.setVisible(False)
                self.display_message(3, "Records Displayed", "Fetch Status")

            else:
                self.loading.setVisible(False)
                self.display_message(2, return_value, "Fetch Status")

        else:
            self.loading.setVisible(False)
            self.display_message(2, "You must select a location to display", "Fetch Status")

            # QMessageBox.critical(
            #     self,
            #     "Error",
            #     f"You must select a location to display",
            # )

    def openAddDialog(self):
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

            self.location_combobox.clear()
            self.location_combobox.addItems(populate_location_cbo())

    def bulk_update(self):
        get_list_of_websites.get_website()
        self.location_combobox.clear()
        self.location_combobox.addItems(populate_location_cbo())

    def setup_UI(self):
        """ Setup the main window's GUI """

        # Create Groupbox/add to the Grid layout
        groupbox = QGroupBox("WUnderground Options")
        self.layout.addWidget(groupbox)

        # Create horizontal layout for textbox/button options
        group_box_layout = QGridLayout()
        groupbox.setLayout(group_box_layout)

        # Date picker
        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())

        # Combobox
        self.location_combobox = QComboBox(self)
        self.location_combobox.clear()
        self.location_combobox.addItems(populate_location_cbo())

        # ########################################
        # Add control widgets to horizontal layout
        # ########################################
        self.date_label = QLabel('Select a record date', self)
        self.date_label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        group_box_layout.addWidget(self.date_label, 0, 0, 1, 2)
        group_box_layout.addWidget(self.dateedit, 1, 0, 1, 2)

        self.location_label = QLabel('Select a weather station', self)
        self.location_label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.location_combobox.setCurrentIndex(-1)  # Blank option

        group_box_layout.addWidget(self.location_label, 0, 3, 1, 2)
        group_box_layout.addWidget(self.location_combobox, 1, 3, 1, 2)

        # Create "Fetch Records" button and assign an action
        self.fetchButton = QPushButton("Fetch Records")
        group_box_layout.addWidget(self.fetchButton, 2, 0)
        self.fetchButton.clicked.connect(self.fetch_button_pressed)

        # Create "Add weather station" button and assign an action
        self.addButton = QPushButton("Add weather station")
        self.addButton.clicked.connect(self.openAddDialog)
        group_box_layout.addWidget(self.addButton, 2, 3)

        # Create "Delete" button and assign an action
        self.deleteButton = QPushButton("Delete weather station")
        self.deleteButton.clicked.connect(self.delete_location)
        group_box_layout.addWidget(self.deleteButton, 2, 4)

        # Create "Clear All" button and assign an action
        self.clearAllButton = QPushButton("Clear All")
        group_box_layout.addWidget(self.clearAllButton, 2, 1)
        self.clearAllButton.clicked.connect(self.clear_all_button_pressed)

        # Create "Loading..." image and setVisible = False
        self.loading = QLabel()  # create the QLabel
        group_box_layout.addWidget(self.loading, 3, 0)  # add it to our layout
        self.loading.setAlignment(Qt.AlignCenter)
        self.loading_image = QPixmap('images/loading.png').scaled(80, 80, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.loading.setPixmap(self.loading_image)
        self.loading.setVisible(False)

        # Create "Export to Excel" button, assign an action, add to layout
        self.exportButton = QPushButton("Export Monthly Data To Excel")
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(self.export_to_excel)
        group_box_layout.addWidget(self.exportButton, 3, 1)


        '''#################################'''
        ''' Begin display box setup '''
        '''#################################'''

        # Daily Data
        self.tableD = QTableView()
        self.tableD.setFixedHeight(84)
        self.tableD.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableD.horizontalHeader().setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        daily_data_label = QLabel('Daily Data', self)
        daily_data_label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.layout.addWidget(daily_data_label)
        self.layout.addWidget(self.tableD)

        # Summary Data
        self.summary_data_label = QLabel('Month-to-date Average', self)
        self.summary_data_label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.tableS = QTableView()
        self.tableS.setFixedHeight(84)
        self.tableS.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableS.resizeColumnsToContents()
        self.tableS.horizontalHeader().setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.layout.addWidget(self.summary_data_label)
        self.layout.addWidget(self.tableS)

        # Monthly Data
        self.monthly_data_label = QLabel('Monthly Data', self)
        self.monthly_data_label.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.tableM = QTableView()
        self.tableM.setMinimumHeight(200)
        # self.tableM.setFixedHeight(200)
        self.tableM.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableM.resizeColumnsToContents()
        self.tableM.horizontalHeader().setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.layout.addWidget(self.monthly_data_label)
        self.layout.addWidget(self.tableM)

    # Using the information in the Monthly Data model, export to an XLSX file
    def export_to_excel(self):

        try:
            # Get information from the Monthly Data model
            m = self.tableM.model()

            # Find the last row
            m_last_record = m.rowCount() - 1

            # Weather location from the last row
            curr_location = m.data(m.index(m_last_record, 0))

            # Date from the last row
            curr_date = m.data(m.index(m_last_record, 1))

            # Convert from a string to a date (using the format given from the model)
            dt_curr_date = datetime.strptime(curr_date, '%Y-%m-%d').date()

            # Get the day of the last day of the month
            int_day = dt_curr_date.day

            # Get the first day of the month by subtracting the number of days in the month from the last day in the model
            from_date = str(dt_curr_date - timedelta(days=(int_day - 1)))
            to_date = str(dt_curr_date)

            # Pass the location and time information to query the database and export to excel
            export_to_excel.open_excel(curr_location, from_date, to_date)

        # Error handling
        except Exception as e:
            self.display_message(2, str(e), "No Data")

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

        self.setupUI()

    # Make each letter typed, a capitol letter
    def on_changed(self, text):
        self.locationField.setText(text.upper())

    def setupUI(self):
        """Setup the Add Location dialog's GUI."""
        # Create line edits for data fields
        self.locationField = QLineEdit()
        self.locationField.setObjectName("Location")
        self.locationField.textChanged[str].connect(self.on_changed)

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Location:", self.locationField)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""

        if not self.locationField.text():
            QMessageBox.critical(
                self,
                "Error!",
                f"You must enter a Location",
            )
            self.data = None  # Reset .data
            return

        self.data = self.locationField.text()

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
        self.setWindowIcon(QtGui.QIcon("images/delete-station.png"))
        self.setFixedSize(250, 100)
        self.data = None

        self.setupUI()

    def setupUI(self):
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
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""

        button_reply = QMessageBox()
        button_reply.setWindowTitle("Delete All Data")
        button_reply.setText("This action will remove ALL data related to this weather station\n\n"
                      "Do you want to continue removing this weather station?")

        button_reply.setIcon(QMessageBox.Question)
        button_reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button_reply.setDefaultButton(QMessageBox.No)
        button_reply.setWindowIcon(QtGui.QIcon("images/delete-station.png"))

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


# About the application
class About_Application(QDialog):
    """Add Website location"""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("About Me")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # Remove question mark from header
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowIcon(QtGui.QIcon("images/delete-station.png"))
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
                             "Last Updated: 4/27/2021"
                             )

        button_reply.setIcon(QMessageBox.Information)
        button_reply.setStandardButtons(QMessageBox.Ok)
        button_reply.setDefaultButton(QMessageBox.Ok)

        button_reply.exec_()


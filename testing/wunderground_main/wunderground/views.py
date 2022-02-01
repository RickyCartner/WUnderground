# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout, QVBoxLayout,
    QMainWindow, QWidget,
    QTableView,
    QPushButton, QCheckBox, QLineEdit, QLabel,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox,
)

from .model import ApiModel


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("RP Contacts")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.apiModel = ApiModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.apiModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        # Create buttons
        self.addButton = QPushButton("Add...")
        self.deleteButton = QPushButton("Delete")
        self.clearAllButton = QPushButton("Clear All")

        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)


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
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.tblAPI.setModel(self.apiModel.model)
        self.tblAPI.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblAPI.resizeColumnsToContents()

        self.btnAdd.clicked.connect(self.openAddDialog)

    def openAddDialog(self):
        """Open the Add Contact dialog."""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.apiModel.addAPI(dialog.data)
            self.tblAPI.resizeColumnsToContents()


"""Add Contact dialog."""
class AddDialog(QDialog):

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add API")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        """Setup the Add Contact dialog's GUI."""
        # Create line edits for data fields
        self.apiField = QLineEdit()
        self.apiField.setObjectName("API")
        self.activeField = QLineEdit()
        self.activeField.setObjectName("Active")
        self.noteField = QLineEdit()
        self.noteField.setObjectName("Note")

        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("API:", self.apiField)
        layout.addRow("Active:", self.activeField)
        layout.addRow("Note:", self.noteField)
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
            self.data.append(self.noteField)

        if not self.data:
            return

        super().accept()

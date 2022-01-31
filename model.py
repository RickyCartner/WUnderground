"""This module provides a model to manage the summary and history tables."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class ApiModel:
    def __init__(self):
        self.model = self._display_api_data()

    @staticmethod
    def _display_api_data():
        tableModel = QSqlTableModel()
        tableModel.setTable("tbl_api_key")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("api_key", "primary_api_key", "api_notes")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

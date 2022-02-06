# -*- coding: utf-8 -*-
# wunderground/model.py

"""This module provides a model to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery


class MonthlyModel:
    def __init__(self, station_id, begin_date, end_date):
        self.station_id = station_id
        self.begin_date = begin_date
        self.end_date = end_date
        self.model = self.createModel()

    # @staticmethod
    def createModel(self):
        """Create and set up the model."""
        # tableModel = QSqlTableModel()
        # tableModel.setTable("tbl_weather_data")
        # tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        # tableModel.select()
        # headers = ("api_key", "primary_api_key", "api_notes")
        tableModel = QSqlTableModel()
        # tableModel.setTable("tbl_history")

        tableQuery = QSqlQuery("database\\weather.db")
        tableQuery.prepare("""SELECT * FROM tbl_weather_data 
                            WHERE stationID = :stationID
                            AND obsTimeLocal BETWEEN :begin_date AND :end_date""")
        tableQuery.bindValue(":stationID", self.station_id)
        tableQuery.bindValue(":begin_date", self.begin_date)
        tableQuery.bindValue(":end_date", self.end_date)
        tableQuery.exec()

        tableModel.setQuery(tableQuery)
        tableModel.select()
        headers = ("Station ID", "Record Date", "Temp High", "Temp Low", "Temp Avg"
                   , "Dew Point High", "Dew Point Low", "Dew Point Avg"
                   , "Heat Index High", "Heat Index Low", "Heat Index Avg"
                   , "Speed High", "Speed Low", "Speed Avg"
                   , "Gust High", "Gust Low", "Gust Avg"
                   , "Chill High", "Chill Low", "Chill Avg"
                   , "Pressure Max", "Pressure Min", "Pressure Trend"
                   , "Precipitation Rate", "Precipitation Total")

        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel



class ApiModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        tableModel.setTable("tbl_api_key")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("api_key", "primary_api_key", "api_notes")

        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel

    def addAPI(self, data):
        """Add a contact to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column), field)
        self.model.submitAll()
        self.model.select()


class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("api_key", "primary_api_key", "api_notes")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

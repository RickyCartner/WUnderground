# -*- coding: utf-8 -*-
# wunderground/model.py

"""This module provides a model to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from .database import create_connection


class MonthlyModel:
    def __init__(self, station_id, begin_date, end_date):
        self.station_id = station_id
        self.begin_date = begin_date
        self.end_date = end_date

        # Create a connection to the database
        create_connection("createConnection")

        # Call the method to display weather data in the table model
        self.model = self.create_model()

        # Close the connection to the database
        create_connection("closeDB")

    # @staticmethod
    def create_model(self):
        """Create and set up the model."""
        # table_model = QSqlTableModel()
        # table_model.setTable("tbl_weather_data")
        # table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        # table_model.select()
        # headers = ("api_key", "primary_api_key", "api_notes")
        table_model = QSqlTableModel()
        # table_model.setTable("tbl_history")

        table_query = QSqlQuery("weather.db")
        print(table_query.isActive())

        table_query.prepare("""SELECT * FROM tbl_weather_data 
                            WHERE stationID = :stationID
                            AND obsTimeLocal BETWEEN :begin_date AND :end_date""")
        table_query.bindValue(":stationID", self.station_id)
        table_query.bindValue(":begin_date", self.begin_date)
        table_query.bindValue(":end_date", self.end_date)
        table_query.exec()
        print(table_query.first())

        table_model.setQuery(table_query)
        table_model.select()
        headers = ("Station ID", "Record Date", "Temp High", "Temp Low", "Temp Avg"
                   , "Dew Point High", "Dew Point Low", "Dew Point Avg"
                   , "Heat Index High", "Heat Index Low", "Heat Index Avg"
                   , "Speed High", "Speed Low", "Speed Avg"
                   , "Gust High", "Gust Low", "Gust Avg"
                   , "Chill High", "Chill Low", "Chill Avg"
                   , "Pressure Max", "Pressure Min", "Pressure Trend"
                   , "Precipitation Rate", "Precipitation Total")

        for columnIndex, header in enumerate(headers):
            table_model.setHeaderData(columnIndex, Qt.Horizontal, header)

        return table_model



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

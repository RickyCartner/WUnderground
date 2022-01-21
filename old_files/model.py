"""This module provides a model to manage the summary and history tables."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery


class DailyModel:
    def __init__(self, location, record_date):
        self.model = self._create_daily_model(location, record_date)

    @staticmethod
    def _create_daily_model(location, record_date):
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        # tableModel.setTable("tbl_history")

        tableQuery = QSqlQuery("weather.db")
        tableQuery.prepare("""SELECT location, record_date, temp_high||' F', temp_avg||' F', temp_low||' F'
                                , dew_point_high||' F', dew_point_avg||' F', dew_point_low||' F'
                                , humidity_high||' %', humidity_avg||' %', humidity_low||' %'
                                , speed_high||' mph', speed_avg||' mph', speed_low||' mph'
                                , pressure_high||' in', pressure_low||' in', precipitation||' in'
                                , date_added 
                                FROM tbl_history 
                                WHERE location = :location
                                AND record_date = :record_date """)
        tableQuery.bindValue(":location", location)
        tableQuery.bindValue(":record_date", record_date)
        tableQuery.exec()

        tableModel.setQuery(tableQuery)
        tableModel.select()
        headers = ("Location", "Record Date", "Temp High", "Temp Avg", "Temp Low"
                   , "Dew Point High", "Dew Point Avg", "Dew Point Low"
                   , "Humidity High", "Humidity Avg", "Humidity Low"
                   , "Speed High", "Speed Avg", "Speed Low"
                   , "Pressure High", "Pressure Low", "Precipitation"
                   , "Date Added")

        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel


class SummaryModel:
    def __init__(self, location, begin_date, end_date):
        self.model = self._create_summary_model(location, begin_date, end_date)

    @staticmethod
    def _create_summary_model(location, begin_date, end_date):
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        # tableModel.setTable("tbl_summary")

        tableQuery = QSqlQuery()
        tableQuery.prepare("""SELECT location, :month_begin, :month_end
                        , round(avg(temp_high),1)||' F', round(avg(temp_low),1)||' F'
                        , round(avg(dew_point_high),1)||' F', round(avg(dew_point_low),1)||' F'
                        , round(avg(humidity_high),0)||' %', round(avg(humidity_low),0)||' %'
                        , round(avg(speed_high),1)||' mph', round(avg(speed_low),1)||' mph'
                        , round(avg(pressure_high),1)||' in', round(avg(pressure_low),1)||' in'
                        , round(avg(precipitation),1)||' in'
                        FROM tbl_history
                        WHERE location = :location
                        AND record_date BETWEEN :begin_date AND :end_date """)

        tableQuery.bindValue(":location", location)
        tableQuery.bindValue(":begin_date", begin_date)
        tableQuery.bindValue(":end_date", end_date)
        tableQuery.bindValue(":month_begin", begin_date)
        tableQuery.bindValue(":month_end", end_date)
        tableQuery.exec()

        tableModel.setQuery(tableQuery)
        tableModel.select()
        headers = ("Location", "Begin Date", "End Date", "Temp High", "Temp Low"
                   , "Dew Point High", "Dew Point Low"
                   , "Humidity High", "Humidity Low"
                   , "Speed High", "Speed Low"
                   , "Pressure High", "Pressure Low"
                   , "Precipitation")

        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel


class MonthlyModel:
    def __init__(self, location, begin_date, end_date):
        self.model = self._create_monthly_model(location, begin_date, end_date)

    @staticmethod
    def _create_monthly_model(location, begin_date, end_date):
        """Create and set up the model."""

        tableModel = QSqlTableModel()
        # tableModel.setTable("tbl_history")

        tableQuery = QSqlQuery()
        tableQuery.prepare("""SELECT location, record_date, temp_high||' F', temp_avg||' F', temp_low||' F'
                        , dew_point_high||' F', dew_point_avg||' F', dew_point_low||' F'
                        , humidity_high||' %', humidity_avg||' %', humidity_low||' %'
                        , speed_high||' mph', speed_avg||' mph', speed_low||' mph'
                        , pressure_high||' in', pressure_low||' in', precipitation||' in'
                        , date_added 
                        FROM tbl_history
                        WHERE location = :location
                        AND record_date BETWEEN :begin_date AND :end_date """)

        tableQuery.bindValue(":location", location)
        tableQuery.bindValue(":begin_date", begin_date)
        tableQuery.bindValue(":end_date", end_date)
        tableQuery.exec()

        tableModel.setQuery(tableQuery)
        tableModel.select()
        headers = ("Location", "Record Date", "Temp High", "Temp Avg", "Temp Low"
                   , "Dew Point High", "Dew Point Avg", "Dew Point Low"
                   , "Humidity High", "Humidity Avg", "Humidity Low"
                   , "Speed High", "Speed Avg", "Speed Low"
                   , "Pressure High", "Pressure Low", "Precipitation"
                   , "Date Added")

        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)

        return tableModel


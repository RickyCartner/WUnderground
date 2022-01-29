# -*- coding: utf-8 -*-

"""This module provides database connections and performs all database transactions"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime
# from datetime import date
import sqlite3


class DB(object):
    def __init__(self, database='database/weather.db', statements=None):
        if statements is None:
            statements = []
        """Initialize a new or connect to an existing database.

        Accept setup statements to be executed.
        """

        # the database filename
        self.database = database
        # holds incomplete statements
        self.statement = ''
        # indicates if selected data is to be returned or printed
        self.display = False

        self.connect()

        # execute setup statements
        # self.execute(statements)

        # self.close()

    def connect(self):
        """Connect to the SQLite3 database."""

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connected = True
        self.statement = ''

    def close(self):
        """Close the SQLite3 database."""

        self.connection.commit()
        self.connection.close()
        self.connected = False

    def fetch_api_key(self):

        self.cursor.execute("SELECT api_key FROM tbl_api_key "
                             "WHERE primary_api_key = 1")

        api_key = self.cursor.fetchone()

        return api_key

    def fetch_all_api_keys(self):

        self.cursor.execute("SELECT * FROM tbl_api_key")

        api_keys = self.cursor.fetchall()
        api_keys_new = []

        # convert tuple to list, replace 1 and 0 values with Yes/No, convert back to tuple
        for api in api_keys:
            api = list(api)
            api = ['Yes' if i==1 else 'No' if i == 0 else i for i in api]
            api = tuple(api)
            api_keys_new.append(api)

        return api_keys_new

    def delete_api_key(self, api_key):

        self.cursor.execute("SELECT api_key FROM tbl_api_key "
                                      "WHERE api_notes = 'generic api key'")
        result = self.cursor.fetchone()
        generic = str(result[0])

        if result[0] == api_key:
            return 'Cannot delete the Public key, you can only update it'

        self.cursor.execute("DELETE FROM tbl_api_key where api_key = ?", [api_key])
        if self.cursor.rowcount > 0:
            self.connection.commit()
            status = 'success'

        self.cursor.execute("UPDATE tbl_api_key SET primary_api_key = 1 "
                            "WHERE api_notes = 'generic api key'")

        return status

    def add_api_key(self, api_key, active):

        self.cursor.execute("INSERT INTO tbl_api_key (api_key, primary_api_key) "
                            "VALUES (?, ?)", (api_key, active))

        if self.cursor.rowcount > 0:
            self.connection.commit()
            status = 'success'
        else:
            status = 'fail insert'

        # clear the key indicator only if the new api key should be primary
        if active:
            self.cursor.execute("UPDATE tbl_api_key SET primary_api_key = 0 "
                                "WHERE primary_api_key = 1 "
                                "AND api_key <> ?", [api_key])

        self.connection.commit()

        return status

    def execute(self, data):
        sql = '''
                INSERT OR IGNORE INTO tbl_weather_data ('stationID', 'obsTimeLocal'
                    , 'tempHigh', 'tempLow', 'tempAvg'
                    , 'windspeedHigh', 'windspeedLow', 'windspeedAvg'
                    , 'windgustHigh', 'windgustLow', 'windgustAvg'
                    , 'dewptHigh', 'dewptLow', 'dewptAvg'
                    , 'windchillHigh', 'windchillLow', 'windchillAvg'
                    , 'heatindexHigh', 'heatindexLow', 'heatindexAvg'
                    , 'pressureMax', 'pressureMin', 'pressureTrend'
                    , 'precipRate', 'precipTotal')
                VALUES(:stationID, :obsTimeLocal
                    , :tempHigh, :tempLow, :tempAvg
                    , :windspeedHigh, :windspeedLow, :windspeedAvg
                    , :windgustHigh, :windgustLow, :windgustAvg
                    , :dewptHigh, :dewptLow, :dewptAvg
                    , :windchillHigh, :windchillLow, :windchillAvg
                    , :heatindexHigh, :heatindexLow, :heatindexAvg
                    , :pressureMax, :pressureMin, :pressureTrend
                    , :precipRate, :precipTotal)
            '''
        self.cursor.executemany(sql, data)
        self.connection.commit()

    # def execute(self, statements):
    #     """Execute complete SQL statements.
    #
    #     Incomplete statements are concatenated to self.statement until they
    #     are complete.
    #
    #     Selected data is returned as a list of query results. Example:
    #
    #     for result in db.execute(queries):
    #         for row in result:
    #             print row
    #     """
    #
    #     queries = []
    #     close = False
    #     if not self.connected:
    #         # open a previously closed connection
    #         self.connect()
    #         # mark the connection to be closed once complete
    #         close = True
    #     if type(statements) == str:
    #         # all statements must be in a list
    #         statements = [statements]
    #     for statement in statements:
    #         if self.incomplete(statement):
    #             # the statement is incomplete
    #             continue
    #         # the statement is complete
    #         try:
    #             statement = self.statement.strip()
    #             # reset the test statement
    #             self.statement = ''
    #             self.cursor.execute(statement)
    #             # retrieve selected data
    #             data = self.cursor.fetchall()
    #             if statement.upper().startswith('SELECT'):
    #                 # append query results
    #                 queries.append(data)
    #
    #         except sqlite3.Error as error:
    #             print
    #             'An error occurred:', error.args[0]
    #             print
    #             'For the statement:', statement
    #
    #     # only close the connection if opened in this function
    #     if close:
    #         self.close()
    #         # print results for all queries
    #     if self.display:
    #         for result in queries:
    #             if result:
    #                 for row in result:
    #                     print
    #                     row
    #             else:
    #                 print
    #                 result
    #     # return results for all queries
    #     else:
    #         return queries


def create_location_table():
    """Create the location table in the database."""
    create_table_query = QSqlQuery()
    # create_table_query.exec("""DROP TABLE tbl_location""")

    create_table_query.exec(
        """
        CREATE TABLE IF NOT EXISTS tbl_location (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            location VARCHAR(11) UNIQUE NOT NULL,
            active INTEGER(1), 
            date_added DATE
        )
        """
    )

    create_table_query.finish()


def create_weather_data_table():

    create_table_query = QSqlQuery()

    create_table_query.exec(
        """
        CREATE TABLE tbl_weather_data (
            'stationID' VARCHAR(11) NOT NULL
            , 'obsTimeLocal' DATE
            , 'tempHigh' DECIMAL(3,1)
            , 'tempLow' DECIMAL(3,1)
            , 'tempAvg' DECIMAL(3,1)
            , 'windspeedHigh' DECIMAL(3,1)
            , 'windspeedLow' DECIMAL(3,1)
            , 'windspeedAvg' DECIMAL(3,1)
            , 'windgustHigh' DECIMAL(3,1)
            , 'windgustLow' DECIMAL(3,1)
            , 'windgustAvg' DECIMAL(3,1)
            , 'dewptHigh' DECIMAL(3,1)
            , 'dewptLow' DECIMAL(3,1)
            , 'dewptAvg' DECIMAL(3,1)
            , 'windchillHigh' DECIMAL(3,1)
            , 'windchillLow' DECIMAL(3,1)
            , 'windchillAvg' DECIMAL(3,1)
            , 'heatindexHigh' DECIMAL(3,1)
            , 'heatindexLow' DECIMAL(3,1)
            , 'heatindexAvg' DECIMAL(3,1)
            , 'pressureMax' DECIMAL(3,1)
            , 'pressureMin' DECIMAL(3,1)
            , 'pressureTrend' DECIMAL(3,1)
            , 'precipRate' DECIMAL(3,1)
            , 'precipTotal' DECIMAL(3,1)
            
            , UNIQUE (stationID, obsTimeLocal)
        )
        """

    )

    create_table_query.finish()


def create_history_table():
    """Create the history table in the database."""
    create_table_query = QSqlQuery()
    # create_table_query.exec("""DROP TABLE tbl_history""")

    create_table_query.exec(
        """
        CREATE TABLE IF NOT EXISTS tbl_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            location VARCHAR(11) NOT NULL,
            record_date DATE NOT NULL,
            temp_high DECIMAL(3,1),
            temp_avg DECIMAL(3,1),
            temp_low DECIMAL(3,1),
            dew_point_high DECIMAL(3,1),
            dew_point_avg DECIMAL(3,1),
            dew_point_low DECIMAL(3,1),
            humidity_high DECIMAL(3,1),
            humidity_avg DECIMAL(3,1),
            humidity_low DECIMAL(3,1),
            speed_high DECIMAL(3,1),
            speed_avg DECIMAL(3,1),
            speed_low DECIMAL(3,1),
            pressure_high DECIMAL(3,2),
            pressure_low DECIMAL(3,2),
            precipitation DECIMAL(3,2),
            date_added DATE,
            
            UNIQUE (location, record_date)
        )
        """
    )

    create_table_query.finish()


def insert_data(table_name, list_data):
    """Insert data into tables."""
    insert_data_query = QSqlQuery()

    if table_name == "history":
        # for list_data in list_data:
        insert_data_query.prepare(
            """
                INSERT INTO tbl_history (location, record_date, temp_high
                                    , temp_avg, temp_low, dew_point_high, dew_point_avg
                                    , dew_point_low, humidity_high, humidity_avg, humidity_low
                                    , speed_high, speed_avg, speed_low
                                    , pressure_high, pressure_low, precipitation
                                    , date_added
                )
                VALUES (:location, :record_date, :temp_high
                        , :temp_avg, :temp_low, :dew_point_high, :dew_point_avg
                        , :dew_point_low, :humidity_high, :humidity_avg, :humidity_low
                        , :speed_high, :speed_avg, :speed_low
                        , :pressure_high, :pressure_low, :precipitation
                        , :date_added
                )
            """
        )

        for l_list in list_data:
            insert_data_query.bindValue(":location", l_list[0])
            insert_data_query.bindValue(":record_date", datetime.strptime(l_list[1], '%m/%d/%Y').strftime('%Y-%m-%d'))
            insert_data_query.bindValue(":temp_high", l_list[2])
            insert_data_query.bindValue(":temp_avg", l_list[3])
            insert_data_query.bindValue(":temp_low", l_list[4])
            insert_data_query.bindValue(":dew_point_high", l_list[5])
            insert_data_query.bindValue(":dew_point_avg", l_list[6])
            insert_data_query.bindValue(":dew_point_low", l_list[7])
            insert_data_query.bindValue(":humidity_high", l_list[8])
            insert_data_query.bindValue(":humidity_avg", l_list[9])
            insert_data_query.bindValue(":humidity_low", l_list[10])
            insert_data_query.bindValue(":speed_high", l_list[11])
            insert_data_query.bindValue(":speed_avg", l_list[12])
            insert_data_query.bindValue(":speed_low", l_list[13])
            insert_data_query.bindValue(":pressure_high", l_list[14])
            insert_data_query.bindValue(":pressure_low", l_list[15])
            insert_data_query.bindValue(":precipitation", l_list[16])
            insert_data_query.bindValue(":date_added", datetime.now().strftime('%Y-%m-%d'))
            insert_data_query.exec()

    elif table_name == "location":

        for l_list in list_data:
            update_location_cbo(l_list[0])

    return


def populate_location_cbo():
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()

    c.execute("SELECT location FROM tbl_location WHERE active = 1 ORDER BY location")
    # rows = c.fetchall()
    list_of_strings = [item[0] for item in c.fetchall()]

    cnn.commit()
    cnn.close()

    return list_of_strings


def update_location_cbo(new_entry):
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()

    c.execute("SELECT COUNT(*) FROM tbl_location WHERE location = ?", [new_entry])

    record_check = c.fetchone()[0]

    if record_check == 0:
        c.execute("INSERT INTO tbl_location (location, active, date_added) VALUES(?, 1, ?)"
                  , (new_entry, datetime.now().strftime('%Y-%m-%d')))

        record_check = "updated"
    cnn.commit()
    cnn.close()

    return record_check

def delete_location(delete_entry):
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()

    # Delete the location
    c.execute("DELETE FROM tbl_location WHERE location = ?", [delete_entry])

    if c.rowcount == 1:
        results = "Delete Successful"
    else:
        results = "Error deleting location"

    cnn.commit()
    cnn.close()

    return results


def delete_history(delete_entry):
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()

    # Check to see if any records exist for this location
    c.execute("SELECT COUNT(*) FROM tbl_history WHERE location = ?", [delete_entry])
    record_check = c.fetchone()[0]

    # If records exist, delete the history data for this location
    if record_check > 0:
        c.execute("DELETE FROM tbl_history WHERE location = ?", [delete_entry])

        if c.rowcount > 0:
            results = "Delete Successful"
        else:
            results = "Error deleting records"
    else:
        results = "Delete Successful"

    cnn.commit()
    cnn.close()

    return results


def fetch_records(location, record_date, table_name):
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()
    if table_name == "tbl_location":
        c.execute("SELECT COUNT(*) FROM tbl_location WHERE location = ? AND record_date = ?", (location, record_date))
    else:
        c.execute("SELECT COUNT(*) FROM tbl_history WHERE location = ? AND record_date = ?", (location, record_date))

    record_count = c.fetchone()[0]

    # list_of_strings = [item[0] for item in c.fetchall()]

    # for row in rows:
    #     ui.comboBox.addItem(str(row[0]))

    cnn.commit()
    cnn.close()

    return record_count


def fetch_history_records(location, from_date, to_date):
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()

    c.execute("SELECT * FROM tbl_history "
              "WHERE location = ? AND record_date BETWEEN ? AND ?", (location, from_date, to_date))

    data_list = c.fetchall()

    # list_of_strings = [item[0] for item in c.fetchall()]

    cnn.commit()
    cnn.close()

    return data_list




def databaseConnection(database_name, action, table_name, list_data):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")   # DB Driver type. QSQLITE = SQLite3 Driver
    connection.setDatabaseName(database_name)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Weather Data",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    if action == "create":
        # Create tables if they don't exist
        create_location_table()
        create_history_table()

    elif action == "insert":
        # insert_template()
        insert_data(table_name, list_data)

    elif action == "delete":
        print("TODO")

    elif action == "close":
        # Clean up the database connections
        connection.close()
        QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

    return True

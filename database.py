# -*- coding: utf-8 -*-

"""This module provides database connections and performs all database transactions"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime
# from datetime import date
import sqlite3


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

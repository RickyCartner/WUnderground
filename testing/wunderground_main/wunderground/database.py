# -*- coding: utf-8 -*-
# wunderground/database.py

"""This module provides a database connection."""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sqlite3


def _createApiTable():
    """Create the contacts table in the database."""
    createApiQuery = QSqlQuery()
    return createApiQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS tbl_api_key (
            api_key VARCHAR(40) PRIMARY KEY UNIQUE NOT NULL,
            active BOOLEAN NOT NULL,
            api_type VARCHAR(50)
        )
        """
    )


# def create_connection(database_name: str, action: str):
def create_connection(action: str):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName('database\\weather.db')

    if not connection.open():
        QMessageBox.warning(
            None,
            "API Key",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    try:
        if action == 'createAPI':
            # Attempt to create the API table
            _createApiTable()
        elif action == 'closeDB':
            # Clean up the database connections
            connection.close()
            QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

    except Exception as e:
        return e

    return True


def populate_location_cbo():
    cnn = sqlite3.connect("database/weather.db")
    c = cnn.cursor()

    c.execute("SELECT location FROM tbl_location WHERE active = 1 ORDER BY location")
    # rows = c.fetchall()
    list_of_strings = [item[0] for item in c.fetchall()]

    cnn.commit()
    cnn.close()

    return list_of_strings


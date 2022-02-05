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


def createConnection(databaseName):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "API Key",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    # Attempt to create the API table
    _createApiTable()

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


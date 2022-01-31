# -*- coding: utf-8 -*-
# wunderground/database.py

"""This module provides a database connection."""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


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

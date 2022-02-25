# -*- coding: utf-8 -*-
# wunderground/main.py

""" This module provides the WUnderground application """

# Standard library imports
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Third party imports
from PyQt5.QtWidgets import QApplication

# Local imports
from wunderground.database import create_connection, DB
from wunderground.views import Window #, ApiUi


def main():
    """ WUnderground main function."""
    # Create the application
    app = QApplication(sys.argv)

    # Connect to the database before creating any window
    # if not create_connection("database\\weather.db", "createConnection"):
    if not create_connection("createConnection"):
        sys.exit(1)

    '''
    TODO: Need to create a module that will attempt to create the database
        tables if they do not currently exist. I.E. The database was accidentally
        deleted.
    '''
    # Reset temp table for new population
    db = DB()
    db.delete_records_from_location_temp()
    db.close()

    # Create the main window
    win = Window()
    win.show()

    # Create the api token window
    # apiwin = ApiUi()
    # apiwin.show()

    # Run the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

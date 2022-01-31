# -*- coding: utf-8 -*-
# rpcontacts/main.py

"""This module provides RP Contacts application."""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from PyQt5.QtWidgets import QApplication
from .database import createConnection
from .views import Window, ApiUi



def main():
    """RP Contacts main function."""
    # Create the application
    app = QApplication(sys.argv)

    # Connect to the database before creating any window
    if not createConnection("database\\weather.db"):
        sys.exit(1)

    # Create the main window
    # win = Window()
    # win.show()

    # Create the api window
    apiwin = ApiUi()
    apiwin.show()

    # Run the event loop
    sys.exit(app.exec_())

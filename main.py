"""This module builds the WUnderground application."""

import os
import sys
from PyQt5.QtWidgets import QApplication
from views import Window
from database import databaseConnection


# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception as e:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)


def main_qt():
    """WUnderground main function."""
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    win = Window()

    # Set the size of the window
    # win.setFixedHeight(700)
    # win.setFixedWidth(900)

    # Display the window
    win.show()

    # # Create the database and tables
    # if not databaseConnection("database/weather.db", "create", "", ""):
    #     sys.exit(1)

    # Execute the application
    app.exec()


def main():

    # Create the folder for the database if it does not exist
    if not os.path.exists("database/weather.db"):
        os.mkdir("database")

    # Create the database and tables
    if not databaseConnection("database/weather.db", "create", "", ""):
        sys.exit(1)

    main_qt()

    databaseConnection("database/weather.db", "close", "", "")


if __name__ == "__main__":
    main()

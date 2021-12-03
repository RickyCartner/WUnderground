#!/usr/bin/env python3
"""This module gets the list of websites to search and inputs them into a list."""


import os
import csv
import database
# import sys
from PyQt5.QtWidgets import QFileDialog, QMainWindow #QApplication, QWidget, QInputDialog, QLineEdit,
# from PyQt5.QtGui import QIcon


class Sheet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.open_sheet()

    def open_sheet(self):
        global file_location

        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            file_location = path[0]
            # print(path[0])



def begin_file_dialog():
    ex = Sheet()


def get_website():
    web_list = []

    try:
        # Call file picker
        begin_file_dialog()

        # Use file that was selected in the previous step (this is a global variable)
        with open(file_location, newline="") as file:
            reader = csv.reader(file)
            # next(reader, None)  # skip the header row

            for row in reader:
                if len(row) != 0:
                    web_list.append(row)

        database.insert_data("location", web_list)
        database.populate_location_cbo()

    except NameError:
        print("No File selected")

    except Exception as e:
        print("An unexpected error occurred", e)
        print(type(e), e)



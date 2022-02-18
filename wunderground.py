#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# wunderground_project/wunderground.py

"""This module provides WUnderground entry point script."""

# from wunderground.main import main


def entry_menu():
    msg = int(input('''
        Enter a menu option below:
        1) Run main application
        2) Run multi_station_picker
        Option: '''))

    if msg == 1:
        from wunderground.main import main
        main()
    elif msg == 2:
        from ui import multi_station_picker as msp
        msp.main()
    else:
        print('Invalid entry')


if __name__ == "__main__":
    entry_menu()
    # main()

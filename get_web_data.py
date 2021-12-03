
import requests
# import urllib.request
from bs4 import BeautifulSoup
# import sys   # Used for exiting early
import datetime
import database
# from database import databaseConnection
import re


def check_for_date(value_check):

    try:
        month, day, year = value_check.split('/')
        isValidDate = True

        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    return isValidDate


def get_web_data(web_alias_list, from_date, to_date, interval):

    row_type = [['precipitation'], ['daily']]
    rows = []
    for alias in web_alias_list:
        url = 'https://www.wunderground.com/dashboard/pws/' + alias + '/table/' \
              + from_date + '/' + to_date + '/' + interval

        # print(url)
        rows = []

        try:

            # Navigate to the website201
            response = requests.get(url)

            # Load all of the HTML data into memory
            source = BeautifulSoup(response.text, "html.parser")

            # ##############################
            # Check if station is Offline
            # ##############################
            status = source.find('div', class_='dashboard__title ng-star-inserted')
            for d in status.find_all('div'):
                s = d.find_all('span')

                # Find the second Span tag in the Div. It should have the status
                station_status = s[1].get_text(strip=True)

                if station_status == "Offline":
                    error_type = "No web data available - Station is Offline"
                    return error_type

            # ########################
            # GET MONTHLY TABLE DATA
            # ########################




            # Reset list
            rows = []

            history = source.find('table', class_='history-table desktop-table')

            for row in history.find_all('tr'):
                temp = []
                cols = row.find_all('td')

                if len(cols) > 1:
                    for col in cols:
                        col_value = col.get_text(strip=True)
                        if check_for_date(col_value):
                            temp.append(col_value)
                        else:
                            # temp.append(col.get_text(strip=True))

                            # This will replace unicode characters, the degree symbol (\u00b0) and a % sign
                            # with an empty space ("").
                            value_only = re.sub("[a-zA-Z\u00b0%]", "", col_value)
                            temp.append(float(value_only))

                    # temp.insert(0, alias[0])  # Started parsing each alias letter?
                    temp.insert(0, alias)
                    rows.append(temp)

            # Insert values into database
            database.insert_data("history", rows)

        # Error handling
        except Exception as e:
            if str(e) == "'NoneType' object has no attribute 'find_all'":
                error_type = "No web data available"
                return error_type
            else:
                print("An unexpected error occurred", e)
                print(type(e), e)
                error_type = e
                # sys.exit()  # Exit the system on this error
                return error_type

    return rows

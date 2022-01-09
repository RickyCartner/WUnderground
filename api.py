"""
Import data from WUnderground using API call
"""

import requests
import json
from datetime import date
import sqlite3 

class Database:
	def __init__(self):
		database_name = "database/weather_data.db"
		load_date = date.today().isoformat()

	def create_table(self):
		conn = sqlite3.connect(self.database_name)
		c = conn.cursor()

	    # c.execute("""CREATE TABLE IF NOT EXISTS tbl_weather_detail (
					# location VARCHAR(11) PRIMARY KEY NOT NULL,
					# weather_date DATE NOT NULL,

					# temp_high DECIMAL(3,1),
					# temp_low DECIMAL(3,1),
					# temp_avg DECIMAL(3,1),

					# wind_speed_high DECIMAL(3,1),
					# wind_speed_avg DECIMAL(3,1),
					# wind_speed_low DECIMAL(3,1),

					# wind_gust_high DECIMAL(3,1),
					# wind_gust_low DECIMAL(3,1),
					# wind_gust_avg DECIMAL(3,1),

					# dew_point_high DECIMAL(3,1),
					# dew_point_low DECIMAL(3,1),
					# dew_point_avg DECIMAL(3,1),

					# wind_chill_high DECIMAL(3,1),
					# wind_chill_low DECIMAL(3,1),
					# wind_chill_avg DECIMAL(3,1),

					# heat_index_high DECIMAL(3,1),
					# heat_index_low DECIMAL(3,1),
					# heat_index_avg DECIMAL(3,1),

					# pressure_max DECIMAL(3,1),
					# pressure_min DECIMAL(3,1),
					# pressure_trend DECIMAL(3,1)

					# precipitation_rate DECIMAL(3,2),
					# precipitation_total DECIMAL(3,2),

					# date_added DATE DEFAULT (datetime('now', 'localtime')),

					# UNIQUE (location, weather_date)
					# )
		   #      """
     #    		)

	    # c.execute("SELECT * FROM tbl_history "
	    #           "WHERE location = ? AND record_date BETWEEN ? AND ?", (location, from_date, to_date))

	    # data_list = c.fetchall()

	    # list_of_strings = [item[0] for item in c.fetchall()]

		conn.commit()
		conn.close()

		return 

	def insert_data(self, column_list, value_list):
		conn = sqlite3.connect(self.database_name)
		c = conn.cursor()

		c.executemany('INSERT INTO tbl_weather_detail (?) VALUES (?)', column_list, value_list)

	    # c.execute("SELECT * FROM tbl_history "
	    #           "WHERE location = ? AND record_date BETWEEN ? AND ?", (location, from_date, to_date))

	    # data_list = c.fetchall()

	    # list_of_strings = [item[0] for item in c.fetchall()]

		conn.commit()
		conn.close()


API_KEY = "e1f10a1e78da46f5b10a1e78da96f525"  # Found on website
# API_KEY = "c6a212d5b8d24b8ba212d5b8d21b8b56"  # Assigned

def current_data(station_id, number_type = "decimal"):

	payload = {"stationId": station_id, "format": "json", "units": "e", 
			"apiKey": API_KEY, "numericPrecision": number_type}

	api_url = 'https://api.weather.com/v2/pws/observations/current'

	response = requests.get(api_url, params=payload)

	station_dict = response.json() 

	key_list = []  # field names
	value_list = [] # values

	for station_info in station_dict['observations']:
		key_list = [key for key, value in station_info['imperial'].items()]
		value_list = [value for key, value in station_info['imperial'].items()]

		station_id = station_info['stationID']
		weather_date = station_info['obsTimeLocal']

		# key_list.insert(0, station_info['stationID'])
		value_list.insert(0, station_id)
		value_list.insert(1, weather_date)

		# print(key_list)
		print(value_list)


def history_day(station_id, search_date = date.today().strftime("%Y%m%d"), number_type = "decimal"):
	payload = {"stationId": station_id, "format": "json", "units": "e", "date":search_date, 
			"apiKey": API_KEY, "numericPrecision": number_type}

	api_url = 'https://api.weather.com/v2/pws/history/daily'

	response = requests.get(api_url, params=payload)

	station_dict = response.json() 

	# print(station_dict)

	key_list = []  # field names
	value_list = [] # values

	for station_info in station_dict['observations']:
		key_list = [key for key, value in station_info['imperial'].items()]
		value_list = [value for key, value in station_info['imperial'].items()]

		station_id = station_info['stationID']
		weather_date = station_info['obsTimeLocal']

		# key_list.insert(0, station_info['stationID'])
		value_list.insert(0, station_id)
		value_list.insert(1, weather_date)

		# print(key_list)
		print(search_date)
		print(value_list)

def history_7_day(station_id, number_type = "decimal"):

	payload = {"stationId": station_id, "format": "json", "units": "e", 
			"apiKey": API_KEY, "numericPrecision": number_type}

	api_url = 'https://api.weather.com/v2/pws/dailysummary/7day'

	response = requests.get(api_url, params=payload)

	station_dict = response.json() 

	key_list = []  # field names
	value_list = [] # values

	for station_info in station_dict['summaries']:

		station_id = station_info['stationID']
		weather_date = station_info['obsTimeLocal']


		key_list = [key for sort_values(key, value) in station_info['imperial'].items()]
		print(key_list)
		# key_list = [key for key, value in station_info['imperial'].items()]
		# value_list = [value for key, value in station_info['imperial'].items()]

		# value_list.insert(0, station_id)
		# value_list.insert(1, weather_date)


		# print(value_list)


def sort_values(key, value):

	print(key, value)

	# location VARCHAR(11) PRIMARY KEY NOT NULL,
	# 	            weather_date DATE NOT NULL,

	# 	            temp_high DECIMAL(3,1),
	# 	            temp_low DECIMAL(3,1),
	# 	            temp_avg DECIMAL(3,1),

	# 	            wind_speed_high DECIMAL(3,1),
	# 	            wind_speed_avg DECIMAL(3,1),
	# 	            wind_speed_low DECIMAL(3,1),

	# 	            wind_gust_high DECIMAL(3,1),
	# 				wind_gust_low DECIMAL(3,1),
	# 				wind_gust_avg DECIMAL(3,1),

	# 				dew_point_high DECIMAL(3,1),
	# 	            dew_point_low DECIMAL(3,1),
	# 	            dew_point_avg DECIMAL(3,1),

	# 				wind_chill_high DECIMAL(3,1),
	# 				wind_chill_low DECIMAL(3,1),
	# 				wind_chill_avg DECIMAL(3,1),

	# 				heat_index_high DECIMAL(3,1),
	# 				heat_index_low DECIMAL(3,1),
	# 				heat_index_avg DECIMAL(3,1),

	# 				pressure_max DECIMAL(3,1),
	# 	            pressure_min DECIMAL(3,1),
	# 	            pressure_trend DECIMAL(3,1)

	# 	            precipitation_rate DECIMAL(3,2),
	# 	            precipitation_total DECIMAL(3,2),

	# 	            date_added DATE DEFAULT (datetime('now', 'localtime')),



if __name__ == "__main__":
	# current_data("KSCBEAUF63")  # KSCBEAUF63, KSCBEAUF78
	# history_day("KSCBEAUF63")
	history_7_day("KSCBEAUF63")
	# print(date.today().strftime("%Y%m%d"))



# print(station_dict['observations'])

# for s in station_dict:
# 	print(s['stationID'])

# for s in station_dict['observations']:
# 	station_id = s.get('stationID')

# 	for x in s['imperial']:
# 		temp = x('temp')
# 		heatIndex = x.get('heatIndex')
# 		dew_point = x.get('dewpt')
# 		wind_chill = x.get('windChill')
# 		wind_speed = x.get('windSpeed')
# 		wind_gust = x.get('windGust')
# 		pressure = x.get('pressure')
# 		precipation_rate = x.get('precipRate')
# 		precipation_total = x.get('precipTotal')

# 	print(station_id)
# 	print(temp)
# 	print(heatIndex)
# 	print(dew_point)
# 	print(wind_chill)
# 	print(wind_speed)
# 	print(wind_gust)
# 	print(pressure)
# 	print(precipation_rate)
# 	print(precipation_total)


# response.status_code
# ?stationId=KSCBEAUF78&format=json&units=e&apiKey=c6a212d5b8d24b8ba212d5b8d21b8b56'

# ?query=beaufort&locationType=pwsid&language=en-US&format=json&apiKey=c6a212d5b8d24b8ba212d5b8d21b8b56'
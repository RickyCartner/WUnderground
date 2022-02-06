"""
Import data from WUnderground using API call
"""

import requests
import json
from datetime import date, datetime, timedelta
import database
import sqlite3
from PyQt5 import uic

#API_KEY = "e1f10a1e78da46f5b10a1e78da96f525"  # Found on website
# API_KEY = "c6a212d5b8d24b8ba212d5b8d21b8b56"  # Assigned

weather_list = []
'''Return data for a specific day'''
def history_day(station_id, search_date = date.today().strftime("%Y%m%d")
				, end_date=date.today().strftime("%Y%m%d"), number_type="decimal"):

	# get the api key
	db = database.DB()
	api_key = db.fetch_api_key()

	while search_date <= end_date:

		querystring = {"stationId": station_id, "format": "json", "units": "e", "date": search_date,
						"apiKey": api_key, "numericPrecision": number_type}

		api_url = 'https://api.weather.com/v2/pws/history/daily'

		response = requests.get(api_url, params=querystring)
		# print(response.json())
		# print(type(response))

		# convert results into dictionary
		station_dict = response.json()
		# station_dict = json.dumps(response.json())
		# print(station_dict)

		# Get a list of Key fields
		value_list = {}
		print(type(value_list))
		# test_list = ['stationID','obsTimeLocal','imperial']
		# res = None
		# if all(sub in [station_dict['observations'], test_list]):
		# 	res = station_dict['observations'][sub]

		# for k, v in station_dict['observations'] if k:
		# 	value_list[k] = v

		for p in station_dict['observations']:
			value_list['stationID'] = p['stationID']
			value_list['obsTimeLocal'] = p['obsTimeLocal']
			value_list.update(p['imperial'])
			# station_id = p['stationID']
			# weather_date = p['obsTimeLocal']
			# value_list = p['imperial']

		# print(value_list)
		# res = {k:v for p in station_dict['observations'] for k, v in p['imperial'].items()}
		# print(res)
		# value_list.update('stationID': station_id)

		# station_id = station_dict['observations']['stationID']
		# weather_date = station_dict['observations']['obsTimeLocal']

		# key_list.insert(0, station_info['stationID'])
		# value_list.update(station_dict['observations']['stationID'])
		# value_list.update(station_dict['observations']['obsTimeLocal'])
		# value_list.insert(0, station_id)
		# value_list.insert(1, weather_date)

		weather_list.append(value_list)
		print(weather_list)

		# print(search_date)
		dto = datetime.strptime(search_date, '%Y%m%d').date()
		search_date = (dto + timedelta(days=1)).strftime("%Y%m%d")

		# print("AFTER 5 DAYS DATE WILL BE : ", search_date)
		# print(date_next)

	db.execute(weather_list)

		# 	else:
		# 		print("All Keys exist but are in the incorrect order")
		# else:
		# 	print("Some Keys are missing")

	db.close()



if __name__ == "__main__":
	# data_list = current_data("KSCBEAUF63")  # KSCBEAUF63, KSCBEAUF78, KCAE (McEntire)
	data_list = history_day("KSCBEAUF63", '20220117')
	# data_list = history_7_day("KSCBEAUF63")
	print(data_list)
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
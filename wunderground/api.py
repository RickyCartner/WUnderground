"""
Import data from WUnderground using API call
"""

import requests
from datetime import date, datetime, timedelta
from wunderground.database import DB


weather_list = []
'''Return data for a specific day'''


def history_day(
		station_id, search_date=date.today().strftime("%Y%m%d"),
		end_date=date.today().strftime("%Y%m%d"), number_type="decimal"):

	# get the api key
	db = DB()
	api_key = db.fetch_api_key()
	# print(api_key)

	while search_date <= end_date:

		# db = database.DBConnection()
		if not db.check_table_for_existing_data(station_id, search_date):

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


			for p in station_dict['observations']:
				value_list['stationID'] = p['stationID']
				value_list['obsTimeLocal'] = p['obsTimeLocal']
				value_list.update(p['imperial'])


			weather_list.append(value_list)
			# print(weather_list)

		# print(search_date)
		dto = datetime.strptime(search_date, '%Y%m%d').date()
		search_date = (dto + timedelta(days=1)).strftime("%Y%m%d")

	db.execute(weather_list)


	db.close()



if __name__ == "__main__":
	# data_list = current_data("KSCBEAUF63")  # KSCBEAUF63, KSCBEAUF78, KCAE (McEntire)
	data_list = history_day("KSCBEAUF63", '20220117')
	# data_list = history_7_day("KSCBEAUF63")
	print(data_list)
	# print(date.today().strftime("%Y%m%d"))

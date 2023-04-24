import requests
import math
from datetime import date, datetime


def get_api_data():
	base_url = "https://api.openweathermap.org/data/2.5/forecast?"
	api_key = "2aefe52a593c0d988f240092f4dfa3c6"
	lon = "121.0745"  # lon from user city form
	lat = "13.7888"


	url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}"

	# get data from owm
	response = requests.get(url).json()

	# convert date to str
	current_date = date.today().isoformat()
	item_per_day = 0
	sum_of_temp = 0
	sum_of_humidity = 0
	sum_of_rain = 0
	formatted_data = [];

	weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

	for i in range(len(response['list'])):

		# print(response['list'][i])

		timestamp = response['list'][i]['dt']
		# convert timestamp to date
		date_ = datetime.fromtimestamp(timestamp)

		# convert date to str
		date_str = date_.strftime('%Y-%m-%d')

		if current_date != date_str:
			current_date = date_str

			formatted_data.append({
				"day_of_week": weekdays[date_.isoweekday() - 2],
				"avg_temp": round((sum_of_temp/ item_per_day) - 273.15),
				"avg_humidity": round(sum_of_humidity/ item_per_day),
				"avg_rain": round(sum_of_rain / item_per_day),
				"weather_string": 1
			})
			item_per_day = 0
			sum_of_temp = 0
			sum_of_humidity = 0
			sum_of_rain = 0

		item_per_day += 1
		sum_of_temp = sum_of_temp + response['list'][i]['main']['temp']
		sum_of_humidity = sum_of_humidity + response['list'][i]['main']['humidity']

		if 'rain' in response['list'][i]:
			sum_of_rain = sum_of_rain + response['list'][i]['rain']['3h']

	print(formatted_data) # use this to change the content of html

	return formatted_data
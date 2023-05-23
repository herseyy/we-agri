import requests
import math
from datetime import date, datetime, timedelta
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("API_KEY")

def get_api_data(lat, lon):
	base_url = "https://api.openweathermap.org/data/2.5/forecast?"
	base_url_current = "https://api.openweathermap.org/data/2.5/weather?"
	# lon = "121.0580992"  # lon from user city form
	# lat = "13.778944"


	url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}"
	url_current = f"{base_url_current}lat={lat}&lon={lon}&appid={api_key}"

	# get data from owm
	response = requests.get(url).json()
	res = requests.get(url_current).json()

	# convert date to str
	tempo_date = datetime.now()
	item_per_day = 0
	sum_of_temp = 0
	sum_of_humidity = 0
	# sum_of_rain = 0
	formatted_data = [];

	weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


	# utc (2am start)
	after_11pm = tempo_date.replace(hour=23, minute=0, second=0, microsecond=0)

	before_2am = tempo_date.replace(hour=2, minute=5, second=0, microsecond=0)

	# convert tempo_date to string
	tempo_date_str = tempo_date.strftime('%Y-%m-%d')

	if tempo_date > after_11pm:
		plus_1 = tempo_date.strptime(tempo_date_str, "%Y-%m-%d") + timedelta(days=1)
		tempo_date_str = plus_1.strftime('%Y-%m-%d')


	for i in range(len(response['list'])):
		timestamp = response['list'][i]['dt']

		# convert timestamp to date
		date_ = datetime.fromtimestamp(timestamp)

		# convert date to str
		date_str = date_.strftime('%Y-%m-%d')
		if tempo_date_str != date_str:
			tempo_date_str = date_str
			formatted_data.append({
				"day_of_week": weekdays[date_.isoweekday() - 2],
				"avg_temp": float(np.round((sum_of_temp / item_per_day) - 273.15, 2)),
				"avg_humidity": float(np.round(sum_of_humidity / item_per_day, 2)),
				"weather_string": 1
			})

			item_per_day = 0
			sum_of_temp = 0
			sum_of_humidity = 0

		item_per_day += 1
		sum_of_temp = sum_of_temp + response['list'][i]['main']['temp']
		sum_of_humidity = sum_of_humidity + response['list'][i]['main']['humidity']

	months = ["January", 
			"February", 
			"March", 
			"April", 
			"May", 
			"June", 
			"July", 
			"August", 
			"September", 
			"October", 
			"November", 
			"December"
		]

	nth_month = datetime.now().month
	current_month = months[nth_month - 1]

	predict = []
	n_plants = 3



	# check temp
	for i in range(len(formatted_data)):
		predict.append(formatted_data[i]["avg_temp"])


	for j in range(len(formatted_data)):
		predict.append(formatted_data[i]["avg_humidity"])

	# eto pag dry season
	if current_month == months[11] \
		or current_month == months[0] \
		or current_month == months[1] \
		or current_month == months[2] \
		or current_month == months[3] \
		or current_month == months[4]:
			predict.append(1)
			predict.append(0)
	else:
		predict.append(0)
		predict.append(1)

	# print(predict)
	# print(training)



	return predict

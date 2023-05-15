import requests
import math
from datetime import date, datetime, timedelta
import numpy as np

def get_api_data():
	base_url = "https://api.openweathermap.org/data/2.5/forecast?"
	base_url_current = "https://api.openweathermap.org/data/2.5/weather?"
	api_key = "2aefe52a593c0d988f240092f4dfa3c6"
	lon = "121.0580992"  # lon from user city form
	lat = "13.778944"


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
	sum_of_rain = 0
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

		# print(date_)
		# print(tempo_date_str)


		# check if time is before 2am

		# if i == 39:
		# 	end_date = date_.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
		# 	# # print(end_date)
		# 	date_str = end_date.strftime('%Y-%m-%d')

		# print(tempo_date_str)
		# print(date_str)

			# pass or ewan

		# print(weekdays[date_.isoweekday() - 2])
		if tempo_date_str != date_str:
			tempo_date_str = date_str
			# print(date_, "a")
			# print(weekdays[date_.isoweekday() - 2])
			# print(sum_of_temp)
			formatted_data.append({
				"day_of_week": weekdays[date_.isoweekday() - 2],
				"avg_temp": float(np.round((sum_of_temp / item_per_day) - 273.15, 2)),
				"avg_humidity": float(np.round(sum_of_humidity / item_per_day, 2)),
				"avg_rain": float(np.round(sum_of_rain / item_per_day, 2)),
				"weather_string": 1
			})

			item_per_day = 0
			sum_of_temp = 0
			sum_of_humidity = 0
			sum_of_rain = 0
		# print(sum_of_temp, "b")
		item_per_day += 1
		sum_of_temp = sum_of_temp + response['list'][i]['main']['temp']
		sum_of_humidity = sum_of_humidity + response['list'][i]['main']['humidity']
		# print(response['list'][i]['main']['temp'])
		# print(sum_of_temp)

		if 'rain' in response['list'][i]:
			sum_of_rain = sum_of_rain + response['list'][i]['rain']['3h']

	# print(formatted_data) # use this to change the content of html

	training = {
		"data": [
			[1, 2, ...],
			[1, 2, ...]
		],
		"label": [
			"okra",
			"etc etc"
		]
	}

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



	# wag na muna isama??? di ko alam pano to AHHAHAHA
	# check rain 
	# for k in range(len(formatted_data)):
	# 	sum_of_rain_5d = 
	# predict.append(3)

	# check season 
	# jun to nov rainy season
	# dec to may dry season

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

	print(predict)



	# veg = 


	# ithrow na para itest
	# pass yung training_data, predict_data, at number of plants
	# var veg = window.predict(training, predict, number_of_plants);
    # var plts = document.getElementById("plants");


	return response

import requests
import math
from datetime import date, datetime, timedelta

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


	for i in range(len(response['list'])):

		timestamp = response['list'][i]['dt']

		# convert timestamp to date
		date_ = datetime.fromtimestamp(timestamp)

		# convert date to str
		date_str = date_.strftime('%Y-%m-%d')


		# check if time is after 11pm
		if tempo_date > after_11pm:
			tempo_date_str = date_str

		# check if time is before 2am
		if tempo_date < before_2am:
			end_date = date_.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
			date_str = end_date.strftime('%m/%d/%Y')

		# print(tempo_date_str, date_str)

		if tempo_date_str != date_str:
			tempo_date_str = date_str

			formatted_data.append({
				"day_of_week": weekdays[date_.isoweekday() - 2],
				"avg_temp": (sum_of_temp/ item_per_day) - 273.15,
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
	print(current_month)

	predict = []
	n_plants = 3

	for i in range(len(formatted_data)):
		print(i)
		predict.append(formatted_data[i]["avg_temp"])

	print(predict)


	         #  for(var i = 0; i < formatted_data.length; i++) {
          #   predict.push(formatted_data[i].avg_temp);
          # }

          # // Check rain here
          #   predict.push(3);

          #   // change true
          #     if (month == 2 || month == 3 || month == 4 || month == 5 ) {
          #       predict.push(1);
          #       predict.push(0);
          #     } 
          #     else {
          #       predict.push(0);
          #       predict.push(1);
          #     }





	return response


import requests


def get_api_data():
	base_url = "https://api.openweathermap.org/data/2.5/forecast?"
	api_key = "2aefe52a593c0d988f240092f4dfa3c6"
	lon = "44.34"  # lon from user city form
	lat = "10.99"


	url = f"{base_url}lat={lat}&lon={lon}&appid={api_key}"

	response = requests.get(url).json()
	print(response)
	return response
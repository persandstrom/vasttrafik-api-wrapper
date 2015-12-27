import requests
import base64
import json
import time

TOKEN_URL = 'https://api.vasttrafik.se/token'
API_BASE_URL = 'https://api.vasttrafik.se/bin/rest.exe/v2'

def fetchToken():
	f = open('etc/credentials.txt', 'r')
	CONSUMER_KEY = f.readline().split('\'')[1]
	CONSUMER_SECRET = f.readline().split('\'')[1]

	headers = {
		'Content-qType': 'application/x-www-form-urlencoded',
		'Authorization': 'Basic ' + base64.b64encode(CONSUMER_KEY + ':' + CONSUMER_SECRET)
	}
	data = {'grant_type': 'client_credentials'}

	response = requests.post(TOKEN_URL, data=data, headers=headers)
	obj = json.loads(response.content)
	return obj['access_token']

class Client:

	def __init__(self, format):
		self.token = fetchToken()
		if format == 'JSON':
			self.format = '&format=json'
		else:
			self.format = ''

	def get_arrivals(self, stopID):
		data = self.get('/arrivalBoard?id=' + str(stopID) + '&date=' + time.strftime("%Y-%m-%d") + 
			'&time=' + time.strftime("%H:%M") + self.format)
		return data['ArrivalBoard']['Arrival']

	def get_departures(self, stopID):
		data = self.get('/departureBoard?id=' + str(stopID) + '&date=' + time.strftime("%Y-%m-%d") + 
			'&time=' + time.strftime("%H:%M") + self.format)
		return data['DepartureBoard']['Departure']

	def search_stops(self, query):
		data = self.get('/location.name?input=' + query + self.format)
		return data['LocationList']['StopLocation']

	def get(self, endpoint):
		url = API_BASE_URL + endpoint
		headers = {
			'Authorization': 'Bearer ' + self.token
		}

		res = requests.get(url, headers=headers)
		if res.status_code == 200:
			return json.loads(res.content, 'UTF-8')
		else:
			raise Exception('Error: ' + str(res.status_code) + res.read())

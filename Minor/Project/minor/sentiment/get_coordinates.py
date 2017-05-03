import requests
import json
import os
from time import time


class Geocoding:

	def __init__(self):
	
		self.baseurl="https://maps.googleapis.com/maps/api/geocode/json?"
		self.key='AIzaSyD2NHusvB7X_kEm3YMWQucu9jVYq23riqA'
	def getLongLat(self,city):
		resultdict={}
		resultdict['city']=city
		payload={'address':resultdict['city'],'key':self.key,'sensor':True}

		jsonstring=requests.get(self.baseurl,payload).text
		
		jsondict=json.loads(jsonstring)
		if jsondict['status']=='OK':
			resultdict['lat']=jsondict['results'][0]['geometry']['location']['lat']
			resultdict['long']=jsondict['results'][0]['geometry']['location']['lng']
			for l in jsondict['results'][0]['address_components']:
				if l['types'][0] == "administrative_area_level_1":
					resultdict['state']=l['long_name']
		return resultdict

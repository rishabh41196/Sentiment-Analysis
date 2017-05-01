import requests
import json
import os
# import pandas as pd
from queue import Queue
from threading import Thread
from time import time


class Geocoding:

	def __init__(self):
	
		self.baseurl="https://maps.googleapis.com/maps/api/geocode/json?"
		self.key='AIzaSyD_kxPXsCwGxiHTSG_lwz9rzdMa-CIM7jg'

	def getLongLat(self,city):
		resultdict={}
		resultdict['city']=city
		payload={'address':resultdict['city'],'key':self.key}
		jsonstring=requests.get(self.baseurl,payload).text
		jsondict=json.loads(jsonstring)

		if jsondict['status']=='OK':
			resultdict['lat']=jsondict['results'][0]['geometry']['location']['lat']
			resultdict['long']=jsondict['results'][0]['geometry']['location']['lng']
			for l in jsondict['results'][0]['address_components']:
				if l['types'][0] == "administrative_area_level_1":
					resultdict['state']=l['long_name']
		return resultdict

geo = Geocoding()
print geo.getLongLat("smofc")
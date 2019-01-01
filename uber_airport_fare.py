# 1/1/19
# Gaurav Gupta
# script to get uber upfront fare to and from airport

import time
import datetime
from uber_rides.session import Session
from uber_rides.session import OAuth2Credential
from uber_rides.client import UberRidesClient

CLIENT_ID = ''
ACCESS_TOKEN = ''
HOME_COORDINATES = (12.963771, 77.646856)
AIRPORT_COORDINATES = (13.197862, 77.707526)

TIME_INTERVAL = 600 # in seconds
OUT_FILE = 'fare_log'
UBER_AIRPORT_POOL = 'Pool Airport'
UBER_GO = 'UberGo'

oauth2credential = OAuth2Credential(client_id=CLIENT_ID, access_token=ACCESS_TOKEN, expires_in_seconds=2592000, scopes={'request'}, grant_type='authorization_code')
session = Session(oauth2credential=oauth2credential)
client = UberRidesClient(session)


def get_uber_fare(uber_type, start_coordinates, end_coordinates, uber_products):
	p_id = None
	for p in uber_products:
		if p['display_name'] == uber_type:
			p_id = p.get('product_id')
			break

	if p_id is None:
		return 'null'

	estimate = client.estimate_ride(
		product_id=p_id,
		start_latitude=start_coordinates[0],
		start_longitude=start_coordinates[1],
		end_latitude=end_coordinates[0],
		end_longitude=end_coordinates[1],
		seat_count=1
	)
	fare = estimate.json.get('fare')
	return fare['value']


def get_uber_products(coordinates):
	response = client.get_products(coordinates[0], coordinates[1])
	products = response.json.get('products')
	return products

if __name__ == '__main__':
	with open(OUT_FILE, 'a') as f: 
		while True:
			try:
				uber_products = get_uber_products(HOME_COORDINATES)
				uber_go_fare = get_uber_fare(UBER_GO, HOME_COORDINATES, AIRPORT_COORDINATES, uber_products)
				uber_airport_pool_fare = get_uber_fare(UBER_AIRPORT_POOL, HOME_COORDINATES, AIRPORT_COORDINATES, uber_products)
				print(str(datetime.datetime.now()) + '\t' + 'D' + '\t' + str(uber_go_fare) + '\t' + str(uber_airport_pool_fare))
				f.write(str(datetime.datetime.now()) + '\t' + 'D' + '\t' + str(uber_go_fare) + '\t' + str(uber_airport_pool_fare) + '\n')

				uber_products = get_uber_products(AIRPORT_COORDINATES)
				uber_go_fare = get_uber_fare(UBER_GO, AIRPORT_COORDINATES, HOME_COORDINATES, uber_products)
				uber_airport_pool_fare = get_uber_fare(UBER_AIRPORT_POOL, AIRPORT_COORDINATES, HOME_COORDINATES, uber_products)
				print(str(datetime.datetime.now()) + '\t' + 'R' + '\t' + str(uber_go_fare) + '\t' + str(uber_airport_pool_fare))
				f.write(str(datetime.datetime.now()) + '\t' + 'R' + '\t' + str(uber_go_fare) + '\t' + str(uber_airport_pool_fare) + '\n')
			except Exception as e:
				print(str(datetime.datetime.now()) + '\t' + 'E' + '\t' + str(e))
				f.write(str(datetime.datetime.now()) + '\t' + 'E' + '\t' + str(e) + '\n')
				pass
			time.sleep(TIME_INTERVAL)

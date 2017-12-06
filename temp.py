import requests
import time
import pprint

pp = pprint.PrettyPrinter(indent = 4)


while True:
		pp.pprint(requests.get(url = "https://uni-apartment-services.herokuapp.com/property").content)
		time.sleep(60)
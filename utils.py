import pandas as pd
from sodapy import Socrata

keys = open('api-key.txt').readlines()
app_key, username, password = [x.strip('\n') for x in keys[0:3]]

client = Socrata("data.cityofberkeley.info", app_key, username=username, password=password)

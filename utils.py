import pandas as pd
from sodapy import Socrata

keys = open('api-key.txt').readlines()
app_key, username, password = keys[0:2]

client = Socrata("data.cityofberkeley.info", app_key, username=username, password=password)

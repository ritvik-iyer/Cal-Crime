import pandas as pd
import numpy as np
from sodapy import Socrata

keys = open('api-key.txt').readlines()
app_key, username, password = [x.strip('\n') for x in keys[0:3]]

client = Socrata("data.cityofberkeley.info", app_key, username=username, password=password)

def load_calls():
    calls = pd.DataFrame.from_records(client.get('k2nh-s5h5', limit = 10000000))
    def get_lat(series):
        """Get latitude values from json dict in column"""
        return [series[x].get('latitude', np.nan) for x in np.arange(len(series))]
    def get_lon(series):
        """Get longitude values from json dict in column"""
        return [series[x].get('longitude', np.nan) for x in np.arange(len(series))]
    calls['x'] = get_lon(calls['block_location'])
    calls['y'] = get_lat(calls['block_location'])
    calls = calls.loc[:, 'blkaddr':][['x', 'y', 'blkaddr', 'offense', 'eventdt', 'eventtm']]
    calls['time'] = calls['eventdt'].str.slice(0, 10) + " " + calls['eventtm']
    calls = calls.dropna()
    calls['time'] = pd.to_datetime(calls['time'])
    calls = calls.drop(columns = ['eventdt', 'eventtm'])
    return calls

def load_stops():
    stops = pd.DataFrame.from_records(client.get('6e9j-pj9p', limit = 10000000))
    return stops

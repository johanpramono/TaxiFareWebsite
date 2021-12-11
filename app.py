import streamlit as st
import requests
import urllib.parse
import datetime
import pandas as pd
import numpy as np

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

def get_geoloc(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    lat = (response[0]["lat"])
    lon = (response[0]["lon"])
    return (lon, lat)

pickup_date = st.date_input("Input pick up date", datetime.date(2012, 10, 6))
pickup_time = st.time_input("Input pick up time", datetime.time(12, 10))
pickup_address = st.text_input("Pickup address", "Empire State Building")
dropoff_address = st.text_input("Dropoff_address","Manhattan")
passenger_count = st.slider('No of Pax',1,5,2)

params = {
'key' : "ADASD", 
'pickup_datetime' : datetime.datetime.combine(pickup_date, pickup_time),
'pickup_longitude' : get_geoloc(pickup_address)[0],
'pickup_latitude' : get_geoloc(pickup_address)[1],
'dropoff_longitude' : get_geoloc(dropoff_address)[0],
'dropoff_latitude' : get_geoloc(dropoff_address)[1],
'passenger_count' : passenger_count
}

url = 'https://taxifare.lewagon.ai/predict'

r = requests.get(url = url, params = params)
prediction = r.json()["prediction"]

st.text(f"Fare = ${round(prediction,2)}")

data = {'lon' : [get_geoloc(pickup_address)[0], get_geoloc(dropoff_address)[0]],
        'lat' : [get_geoloc(pickup_address)[1], get_geoloc(dropoff_address)[1]]}

st.map(pd.DataFrame.from_dict(data).astype('float'))
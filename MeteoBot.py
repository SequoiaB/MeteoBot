import requests
from dotenv import load_dotenv
import os
import time
load_dotenv()
api_key = os.getenv("API_BOT_TOKEN")

def unix_to_datetime(unix_timestamp):
    """
    Converts a Unix timestamp to a human-readable date/time string.
    
    Args:
        unix_timestamp (int or float): The Unix timestamp to be converted.
        
    Returns:
        str: A string representing the human-readable date/time.
    """
    giorno = time.strftime('%d-%m', time.localtime(unix_timestamp))
    ora = time.strftime('%H:%M', time.localtime(unix_timestamp))
    return giorno, ora

city_name = 'padova'
state_code = '35020'
limit = 1

# API endpoint URL
url1 = f'http://api.openweathermap.org/geo/1.0/direct?'

url2 = f'q={city_name}&limit={limit}&appid={api_key}'

url3 = url1+url2
# Send the API request
responseGeo = requests.get(url3)

# Check if the request was successful
if responseGeo.status_code == 200:
    # Get the weather data
    geo_data = responseGeo.json()
    # print(geo_data)
    # Extract relevant weather information
    name = geo_data[0]['name']
    print(name)
    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']
    country = geo_data[0]['country']
    state = geo_data[0]['state']

    print(name, lat, lon, country, state)
else:
    print('Error retrieving geographic data')


tempInfo = {    'lat': lat,
                'lon': lon,
                #'exclude': 0,
                'units': "metric",
                'lang': 0,
                }

# API endpoint URL
url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang={"IT"}&appid={api_key}'

# Send the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the weather data
    weather_data = response.json()

    # print(weather_data)
    # Extract relevant weather information
    #city = weather_data['name']
for i in range(len(weather_data['list'])):
    quando_dt = weather_data['list'][i]['dt']
    #print(quando_dt)
    giorno, ora = unix_to_datetime(quando_dt)

    weather = weather_data['list'][i]['weather']
    weather_id = weather[0]['id']
    weather_main = weather[0]['main']
    weather_description = weather[0]['description']
    weather_icon = weather[0]['icon']

    print(weather)
    text = f"""Dati per il giorno {giorno}, alle ore {ora}

"""
    print(text)
    #temperature = weather_data['main']['temp']
    #description = weather_data['weather'][0]['description']

    # Print the weather information
    #print(f'Weather in {city}:')
    #print(f'Temperature: {temperature}°C')
    #print(f'Description: {description}')

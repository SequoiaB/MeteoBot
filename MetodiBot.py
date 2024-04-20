import requests
from dotenv import load_dotenv
import os
import time, datetime
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

def get_weather_data(city_name, days_min, days_max):
    # API endpoint URL
    url1 = f'http://api.openweathermap.org/geo/1.0/direct?'

    url2 = f'q={city_name}&limit={1}&appid={api_key}'

    url3 = url1+url2
    # Send the API request
    responseGeo = requests.get(url3)

    # Check if the request was successful
    if responseGeo.status_code == 200:
        # Get the weather data
        geo_data = responseGeo.json()
        # Extract relevant weather information
        name = geo_data[0]['name']
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        country = geo_data[0]['country']
        state = geo_data[0]['state']
    else:
        print('Error retrieving geographic data')

    # API endpoint URL
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&lang={"IT"}&units={"metric"}&appid={api_key}'

    # Send the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the weather data
        weather_data = response.json()
    else:
        print('Error retrieving weather data')

    nome_citta = weather_data['city']['name']
    text = f"Ecco le previsioni per {nome_citta}."

    """# aggiungere controllo che sceglie che aggiornamenti dare 
        if days_number == 1:
            # Iterare da 1 a 10 con incremento di 2
            for i in range(0, len(weather_data['list']), 2):
                break
            range(10)"""
    da_quando = 2
    for i in range(1, len(weather_data['list'])):
        min_epoch = mattina_del_giorno(days_min)
        max_epoch = get_future_epoch(days_max)
        quando_dt = weather_data['list'][i]['dt']

        if quando_dt < min_epoch:
            continue
        if quando_dt >= max_epoch:
            break
        giorno, ora = unix_to_datetime(quando_dt)
        # weather
        weather = weather_data['list'][i]['weather']
        weather_id = weather[0]['id']
        weather_main = weather[0]['main']
        weather_description = weather[0]['description']
        weather_icon = weather[0]['icon']
        # misc main
        misc_main = weather_data['list'][i]['main']
        temp = misc_main['temp']
        temp_feels_like = misc_main['feels_like']
        humidity = misc_main['humidity']
        # probability of precipitation
        pop = str(int(weather_data['list'][i]['pop']) * 100) + "%" 
        # Rain volume for last 3 hours, mm
        try:
            rain_v =  weather_data['list'][i]['rain']['3h']
            rain_v = str(rain_v) + str("mm")
        except:
            rain_v= """non ha piovuto"""
        
        text = text + str(f"""Il giorno {giorno}, alle ore {ora},
e' previsto {weather_description}.
Con una temperatura di {temp}°C, percepita come {temp_feels_like}°C.
Probabilita' di precipitazioni: {pop}
Precipitazioni nelle ultime 3 ore: {rain_v}\n
""")
    return text

# ora provo a filtrare per giorno, potremmo usare il quando_dt e lasciare stare quelli che non ci interessano
# ricordando che quando_dt esprime il tempo in "secondi passati dal 01-01-1970"

def get_future_epoch(days):
    """
    Returns the Unix epoch time for the future date after adding the specified number of days.
    
    Args:
        days (int): The number of days to add to the current time.
        
    Returns:
        int: The Unix epoch time for the future date.
    """
    # Get the current Unix epoch time
    current_epoch = time.time()
    
    # Calculate the number of seconds in the specified number of days
    seconds_in_days = days * 24 * 60 * 60
    
    # Add the number of seconds to the current epoch time
    future_epoch = current_epoch + seconds_in_days
    
    return int(future_epoch)

def mattina_del_giorno(giorni_da_aspettare):
    future_epoch = get_future_epoch(giorni_da_aspettare)
    future_date = datetime.datetime.fromtimestamp(future_epoch)
    morning_time = datetime.time(7, 50)  # 7:50 AM
    morning_datetime = datetime.datetime.combine(future_date, morning_time)
    morning_timestamp = morning_datetime.timestamp()
    return morning_timestamp

text = get_weather_data("Bressanone", 1, 5)

print (text)
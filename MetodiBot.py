import requests
from dotenv import load_dotenv
import os
from datetime import timedelta
import time, datetime
import MetodiTg
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
    text = f"*Ecco le previsioni per {nome_citta}*.\n\n"

    for i in range(0, len(weather_data['list'])):
        min_epoch = mattina_del_giorno(days_min)
        max_epoch = get_future_epoch(days_max)
        quando_dt = weather_data['list'][i]['dt']

        if quando_dt <= min_epoch:
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
        
        text = text + str(f"""*Il giorno {giorno}, alle ore {ora}*,
e' previsto *{weather_description}*.
Con una temperatura di {temp}°C, percepita come {temp_feels_like}°C.
Probabilita' di precipitazioni: {pop}
Precipitazioni nelle ultime 3 ore: {rain_v}\n
""")
    return text

def get_weather_data_single_day(city_name, days_from_now):
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
        e_country = MetodiTg.escape_special_chars(country)
        e_state = MetodiTg.escape_special_chars(state)
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
    e_nome_citta = MetodiTg.escape_special_chars(nome_citta)
    text = f"*🪟Ecco le previsioni per _{e_nome_citta}_, {e_state}, {e_country}*🌡️\.\n@meteoSequoiaBot"

    for i in range(0, len(weather_data['list'])):
        min_epoch = mattina_del_giorno(days_from_now)
        max_epoch = mezzanotte_del_giorno(days_from_now)
        quando_dt = weather_data['list'][i]['dt']

        if quando_dt < min_epoch:
            print("dato skippato perche' troppo presto")
            continue
        if quando_dt >= max_epoch:
            print("dato skippato perche' troppo tardi")
            break
        giorno, ora = unix_to_datetime(quando_dt)
        e_giorno = MetodiTg.escape_special_chars(giorno)
        # weather
        weather = weather_data['list'][i]['weather']
        weather_id = weather[0]['id']
        emote = emoticon_for_id(weather_id)
        weather_main = weather[0]['main']
        weather_description = weather[0]['description']
        weather_icon = weather[0]['icon']
        # misc main
        misc_main = weather_data['list'][i]['main']
        temp = misc_main['temp']
        temp_feels_like = misc_main['feels_like']
        e_temp = MetodiTg.escape_special_chars(str(temp))
        e_temp_feels_like = MetodiTg.escape_special_chars(str(temp_feels_like))
        humidity = misc_main['humidity']
        # probability of precipitation
        pop = str(int(float(weather_data['list'][i]['pop']) * 100)) + "%" 
        e_pop = MetodiTg.escape_special_chars(pop)

        text = text + str(f"""\n
> *Il giorno {e_giorno}, alle ore {ora}*,
è previsto *{weather_description}{emote}*\.
Con una temperatura di *{e_temp}°C*""")
        if abs(float(temp)- float(temp_feels_like)) > 1: 
            text = text + str(f""", *percepita come {e_temp_feels_like}°C*""")

        text = text + str(f"""\.\n_Probabilita' di precipitazioni: *{e_pop}*_""")
        # Rain volume for last 3 hours, mm
        try:
            rain_v =  weather_data['list'][i]['rain']['3h']
            rain_v = MetodiTg.escape_special_chars(str(rain_v)) + str("mm")
            text = text + str(f"""\n_Precipitazioni nelle ultime 3 ore: *{rain_v}*_\.""")
        except:
            print("""non ha piovuto""")

    return text

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

def mezzanotte_del_giorno(giorni_da_aspettare):
    future_epoch = get_future_epoch(giorni_da_aspettare)
    future_date = datetime.datetime.fromtimestamp(future_epoch)
    midnight_time = datetime.time(23, 50)  # 7:50 AM
    midnight_datetime = datetime.datetime.combine(future_date, midnight_time)
    midnight_timestamp = midnight_datetime.timestamp()
    return midnight_timestamp

def gestioneGiorni():
    # Ottieni la data corrente
    oggi = datetime.datetime.now()

    # Crea un array per i giorni della settimana
    giorni_settimana = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

    # Calcola i prossimi 7 giorni
    prossimi_giorni = [oggi + timedelta(days=i) for i in range(7)]

    # Formatta l'output nel modo desiderato
    risultato = [[f"{giorni_settimana[data.weekday()]} {data.strftime('%d-%m')}"] for data in prossimi_giorni]
    print(risultato)
    return risultato

def emoticon_for_id(id):
    id = int(id)
    if 200 <= id <= 232:
        return "🌩️"
    if 300 <= id <= 321:
        return "🌧️"
    if id == 500 or id == 501:
        return "☔"
    if id == 511:
        return "🌧️🌨️"
    if 502 <= id <= 504:
        return "🌧️💧"
    if 520 <= id <= 531:
        return "🌧️☂️"
    if 600<= id <= 622:
        return "🌨️❄️"
    if 701 <= id <= 781:
        return "🌫️🌫️"
    if id == 800:
        return "☀️"
    if id == 801:
        return "🌤️🌤️"
    if id == 802:
        return "⛅⛅"
    if id == 803:
        return "🌥️🌥️"
    if id == 804:
        return "☁️☁️"
    

def luoghi_possibili(city_name):
    # API endpoint URL
    url1 = f'http://api.openweathermap.org/geo/1.0/direct?'
    url2 = f'q={city_name}&limit={10}&lang={"IT"}&appid={api_key}'
    url3 = url1+url2
    # Send the API request
    responseGeo = requests.get(url3)

    # Check if the request was successful
    if responseGeo.status_code == 200:
        # Get the weather data
        text ="Ecco le città che ho trovato\n"
        geo_data = responseGeo.json()
        for i in (0, len(geo_data)-1):
            # Extract relevant weather information
            name = geo_data[i]['name']
            lat = geo_data[i]['lat']
            lon = geo_data[i]['lon']
            country = geo_data[i]['country']
            state = geo_data[i]['state']
            e_country = MetodiTg.escape_special_chars(country)
            e_state = MetodiTg.escape_special_chars(state)
            text= text + f"""{e_country}, {e_state}, {name}\n{lat} {lon}\n"""
        print(text)
    else:
        print('Error retrieving geographic data')

luoghi_possibili("Mirano")
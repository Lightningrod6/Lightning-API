import requests
from gtts import gTTS


def get_the_weather(city, state=None, zipcode=None):
    

    if zipcode and zipcode.isdigit():
        search_query = zipcode
    elif city and state:
        search_query = f"{city},{state}"
    else:
        search_query = city
    getting_the_location = requests.get(f"https://geocode.maps.co/search?q={search_query}&api_key=660448520448f880798147kvqca6d18")

    location = getting_the_location.json()
    latitude = location[0]["lat"]
    longitude = location[0]["lon"]

    getting_the_gridpoints = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    
    gridpoints = getting_the_gridpoints.json()

    gridpoint = gridpoints["properties"]["forecast"]

    getting_the_forecast = requests.get(gridpoint)
    print(getting_the_forecast.url)

    forecasts = getting_the_forecast.json()

    wind_direction = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    weather_descriptions = ["Clear", "Mostly Clear", "Partly Cloudy", "Mostly Cloudy", "Cloudy", "Drizzle", "Light Rain", "Rain", "Heavy Rain", "Freezing Rain", "Light Snow", "Snow", "Heavy Snow", "Rain Showers", "Thunderstorms", "Foggy"]
    weather_code_map = {
        0: 0,  # Clear sky
        1: 1, 2: 1, 3: 1,  # Mainly clear, partly cloudy, and overcast
        45: 15, 48: 15,  # Fog and depositing rime fog
        51: 5, 53: 5, 55: 5,  # Drizzle: Light, moderate, and dense intensity
        56: 9, 57: 9,  # Freezing Drizzle: Light and dense intensity
        61: 6, 63: 6, 65: 6,  # Rain: Slight, moderate and heavy intensity
        66: 9, 67: 9,  # Freezing Rain: Light and heavy intensity
        71: 10, 73: 10, 75: 10,  # Snow fall: Slight, moderate, and heavy intensity
        77: 10,  # Snow grains
        80: 13, 81: 13, 82: 13,  # Rain showers: Slight, moderate, and violent
        85: 11, 86: 11,  # Snow showers slight and heavy
        95: 14,  # Thunderstorm: Slight or moderate
        96: 14, 99: 14  # Thunderstorm with slight and heavy hail
    }

    getting_current_weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch")
    current_weather = getting_current_weather.json()
    current_location = gridpoints["properties"]["relativeLocation"]["properties"]["city"]
    print(f"Here is the current weather for {current_location}")
    temperature = current_weather["current"]["temperature_2m"]
    wind_speed = current_weather["current"]["wind_speed_10m"]
    wind_direction = current_weather["current"]["wind_direction_10m"]
    wind_gusts = current_weather["current"]["wind_gusts_10m"]
    weather_code = current_weather["current"]["weather_code"]
    weather_description = weather_descriptions[weather_code_map.get(weather_code, 0)]
    feels_like_temperature = current_weather["current"]["apparent_temperature"]
    if wind_direction == 0:
        wind_directions = "N"
    elif wind_direction in range(1, 89):
        wind_directions = "NE"
    elif wind_direction == 90:
        wind_directions = "E"
    elif wind_direction in range(91, 179):
        wind_directions = "SE"
    elif wind_direction == 180:
        wind_directions = "S"
    elif wind_direction in range (181, 269):
        wind_directions = "SW"
    elif wind_direction == 270:
        wind_directions = "W"
    elif wind_direction in range (271, 359):
        wind_directions = "NW"
    print(f"Right now, it is {temperature} and feels like {feels_like_temperature}. The wind is currently going {wind_directions} at {wind_speed} with gusts up to {wind_gusts}")
    print(getting_current_weather.url)
    print(weather_description)
    for forcast in forecasts["properties"]["periods"]:
        if "Night" in forcast['name']:
            print(f"{forcast['name']}: {forcast['shortForecast']}. Tempeature ranging from a low of {forcast['temperature']}")
        else:
            print(f"{forcast['name']}: {forcast['shortForecast']}. Temperature ranging from a high of {forcast['temperature']}")
    


print(get_the_weather("lawton", "ok"))


# getting_the_location = requests.get(f"https://geocode.maps.co/search?q=lawton,ok&api_key=660448520448f880798147kvqca6d18")

# location = getting_the_location.json()

# latitude = location[0]["lat"]
# longitude = location[0]["lon"]

# print(latitude + longitude)
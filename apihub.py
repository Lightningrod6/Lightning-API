from time import sleep
import json
import requests
from os import getenv
import os
from datetime import datetime
import calendar
from google import generativeai as lightningai



try:
    try:
        import dotenv
    except ModuleNotFoundError:
        print("This module was not found. Go to your console or terminal and do 'pip install dotenv'. If that doesn't work, do 'pip3 install dotenv', then run the python script again.")
    script_dir = os.path.abspath(os.path.dirname(__file__))


    # Construct the absolute path to the .env file
    env_file = os.path.join(script_dir, '.env')
    dotenv.load_dotenv(env_file)
    if not os.path.exists(env_file):
        print("The .env file doesn't exist, creating a new one...")
        with open(env_file, "w") as file:
            file.write("FINNHUB_API_KEY='Your Finnhub API key'\nALPHAVANTAGE_API_KEY='Your Alpha Vantage API key'\nOPENWEATHERMAP_API_KEY='Your OpenWeatherMap API Key'\nGOOGLE_GENERATIVE_API_KEY='Your google ai key'")
            print("Created the .env file. \nThis file may be hidden so make sure your computer can see hidden files.\nGet your api keys here: \nFinnHub: https://finnhub.io\nAlpha Vantage: https://www.alphavantage.co\nOpenWeatherMap: https://openweathermap.org")
    else:
        print("Welcome to the Lightning API Python script. ")
        sleep(2)
        user_choice = input("Which API do you wish to interact with:\n1. Lightning Stocks API,\n2. Lightning Weather API\n3 Lightning AI API: ")

        if user_choice == "1" or user_choice == "Lightning Stocks API" or user_choice == "Lightning Stocks" or user_choice == "Stocks":
            def LightningStockAPI():
                finnhubAPIKey = os.getenv('FINNHUB_API_KEY')
                alphaVantageAPIKey = os.getenv('ALPHAVANTAGE_API_KEY')
                test_finnhub_url = "https://finnhub.io/api/v1/quote?symbol=AAPL&token=" + finnhubAPIKey
                test_alphavantage_url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&token=demo"

                test_urls = requests.get(test_finnhub_url) and (test_alphavantage_url)

                if finnhubAPIKey and alphaVantageAPIKey == "" or len(finnhubAPIKey) > 40 or len(finnhubAPIKey) < 40 and len(alphaVantageAPIKey) > 16 or len(alphaVantageAPIKey) < 16:
                    print("Something isnt right... check your .env file and try again")
                else:
                    if test_urls == 401:
                        print("A 401 code was returned. Check the apikey and try again")
                    else:
                        symbol_choice = input("Enter a stock symbol: ")
                        finnurl = "https://finnhub.io/api/v1/quote?symbol=" + symbol_choice + "&token=" + finnhubAPIKey
                        stock_name = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + symbol_choice + "&apikey=" + alphaVantageAPIKey
                        get_stock_info = requests.get(finnurl)
                        stock_info_data = requests.get(stock_name)

                        stock_data = get_stock_info.json()
                        stock_info_data = stock_info_data.json()
                        if get_stock_info.status_code == 200:
                            if stock_data.get("t") == 0:
                                print("Stock data not found")
                            else:
                                current_price = stock_data["c"]
                                s_name = stock_info_data["Name"]
                                price_change = stock_data["d"]
                                open_price = stock_data["o"]
                                high_price_today = stock_data["h"]
                                low_price_today = stock_data["l"]

                                print(f"Stock information for {s_name}")
                                print(f"Current price: ${current_price}")
                                print(f"Open Price: ${open_price}")
                                print(f"Price Change: ${price_change}")
                                print(f"Todays High Price: ${high_price_today}")
                                print(f"Todays Low Price: ${low_price_today}")
                                    
                        else:
                            print("Failed to fetch stock")
            LightningStockAPI()        
        elif user_choice == "2" or user_choice == "Lightning Weather API" or user_choice == "Lightning Weather" or user_choice == "Weather API" or user_choice == "Weather":
            def LightningWeatherAPI():
                openweathermapAPIKey = os.getenv('OPENWEATHERMAP_API_KEY')
                weather_input = input("Type in a location: ")
                choices = input("Do you want the current weather, the 7 day forecast or hourly forecast? (1, 2 or 3)")
                
                if choices == "1" or choices == "Current" or choices == "Current weather":
                    def GetCurrentWeather():
                        weather_url = "https://api.openweathermap.org/data/2.5/weather?q=" + weather_input + "&units=imperial&appid=" + openweathermapAPIKey
                    

                        weather_request = requests.get(weather_url)
                        if weather_request.status_code == 404:
                            print("Unknown Location")
                        else:
                            weather = weather_request.json()
                            current_temperature = round(weather['main']['temp'])
                            current_feelslike_temperature = round(weather['main']['feels_like'])
                            current_conditions = weather['weather'][0]['main']
                            print("The current weather for " + weather_input)
                            print("Current Temperature: " + str(current_temperature))
                            print("Feels like " + str(current_feelslike_temperature))
                            print("Current conditions: " + current_conditions)
                            print
                    GetCurrentWeather()
                elif choices == "2" or choices == "7 Day" or choices == "7 Day Forecast":
                    def Get7DayForecast():

                        seven_day_forecast_url = "https://api.openweathermap.org/data/2.5/forecast/daily?q=" + weather_input + "&units=imperial&cnt=7&appid=" + openweathermapAPIKey
                        seven_day_request = requests.get(seven_day_forecast_url)
                        if seven_day_request.status_code == 404:
                            print("Unknown location")
                        else:
                            
                            seven_day_forecast = seven_day_request.json()
                            
                            for day in seven_day_forecast['list']:
        # Convert Unix timestamp to datetime object
                                dt_object = datetime.fromtimestamp(day['dt'])
                                
                                # Get the day of the week (Monday is 0, Sunday is 6)
                                day_of_week = dt_object.weekday()
                                
                                # Convert numeric representation to day name
                                day_name = calendar.day_name[day_of_week]
                                
                                temp_min = round(day['temp']['min'])    
                                temp_max = round(day['temp']['max'])
                                conditions = day['weather'][0]['main']
                                
                                print(day_name)
                                print("High: " + str(temp_max))
                                print("Low: " + str(temp_min))
                                print("Weather: " + conditions + "\n")
                    Get7DayForecast()
            LightningWeatherAPI()
        elif user_choice == "3" or user_choice == "AI" or user_choice == "Lightning AI":
            def LightningAIAPI():

                model = lightningai.GenerativeModel('gemini-pro', )
                lightningai.configure(api_key=os.getenv('GOOGLE_GENERATIVE_API_KEY'))
                user_ask = input("Ask the ai something: ")
                user_input = model.generate_content(user_ask)
                if "code" or "program" or "script" or "" in user_ask:
                    print("I see you have asked for a specific program to be created... Before the ai begins coding, what file extension are you planning to use vvv")
                    file_extension = input()
                    file_name = input("Now name the file: ")
                    if file_extension == "js" or file_extension == "javascript":
                        file_extension = ".js"
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output) # Assuming it generates full code including comment blocks
                    elif file_extension == "java":
                        file_extension == ".java"
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'cpp':  # C++
                        file_extension = '.cpp'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'cs':  # C#
                        file_extension = '.cs'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'rb':  # Ruby
                        file_extension = '.rb'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'go':  # Go
                        file_extension = '.go'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'php':  # PHP
                        file_extension = '.php'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'rs':  # Rust
                        file_extension = '.rs'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'kt':  # Kotlin
                        file_extension = '.kt'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'swift':  # Swift
                        file_extension = '.swift'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'ts':  # TypeScript
                        file_extension = '.ts'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'scala':  # Scala
                        file_extension = '.scala'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'groovy':  # Groovy
                        file_extension = '.groovy'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'dart':  # Dart
                        file_extension = '.dart'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'lua':  # Lua
                        file_extension = '.lua'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'pl':  # Perl
                        file_extension = '.pl'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'r':  # R
                        file_extension = '.r'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'sh':  # Shell Script
                        file_extension = '.sh'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'bat':  # Batch File
                        file_extension = '.bat'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'ml':  # OCaml
                        file_extension = '.ml'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'hs':  # Haskell
                        file_extension = '.hs'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'f':  # Fortran
                        file_extension = '.f'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'pas':  # Pascal
                        file_extension = '.pas'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    elif file_extension == 'vb':  # Visual Basic
                        file_extension = '.vb'
                        with open(file_name + file_extension, "w") as code_file:
                            ai_output = user_input.text
                            code_file.write(ai_output)
                    else:
                        print("Invalid File extension, continuing without saving code.")
                        if len(ai_output) > 400:
                            with open("ai_ouput.txt", "a") as ai_file:
                                ai_file.write(ai_output + "-----------------------------\n")
                                print("Response too big, saved to ai_output.txt")
                        else:
                            print(ai_output)
            LightningAIAPI()
except KeyboardInterrupt:
    print("\nExiting...")

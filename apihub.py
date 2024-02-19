
from time import sleep
import json
import requests
from os import getenv
import os

try:
    import dotenv
except ModuleNotFoundError:
    print("This module was not found. Go to your console or terminal and do 'pip install dotenv'. If that doesn't work, do 'pip3 install dotenv', then run the python script again.")

env_file = ".env"
load_env_file = dotenv.load_dotenv()

if not os.path.exists(env_file):
    print("The .env file doesn't exists, creating a new one")
    with open(env_file, "w") as file:
        file.write("FINNHUB_API_KEY='Your Finnhub API key'\nALPHAVANTAGE_API_KEY='Your Alpha Vantage API key'")
else:
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

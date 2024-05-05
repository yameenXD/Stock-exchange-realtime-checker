import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from cachetools import TTLCache

# Constants
API_KEY = 'JI3DCZJISQY0LHYB'  # Replace this with your actual Alpha Vantage API key
API_URL = "https://www.alphavantage.co/query"

# Cache setup for storing API responses
cache = TTLCache(maxsize=100, ttl=86400)  # Cache up to 100 items, each for 1 day

def get_stock_data(symbol, outputsize='compact'):
    if (symbol, outputsize) in cache:
        return cache[(symbol, outputsize)]
    
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": outputsize
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Will raise HTTPError for bad requests
        data = response.json()
        cache[(symbol, outputsize)] = data
        return data
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid Response received."

def parse_stock_data(data, symbol):
    try:
        last_refresh = data['Meta Data']['3. Last Refreshed']
        prices = {date: float(details['4. close']) for date, details in data['Time Series (Daily)'].items()}
        return prices, last_refresh
    except KeyError:
        return {}, "Data format error or missing data"

def plot_stock_data(symbol, days=30):
    data = get_stock_data(symbol, 'compact')
    if isinstance(data, str):
        print(data)
        return

    prices, last_refresh = parse_stock_data(data, symbol)
    if not prices:
        print("No data to display.")
        return

    # Filter to last N days
    end_date = datetime.strptime(last_refresh, '%Y-%m-%d')
    start_date = end_date - timedelta(days=days)
    filtered_prices = {date: price for date, price in prices.items() if datetime.strptime(date, '%Y-%m-%d') >= start_date}

    dates = list(filtered_prices.keys())
    values = list(filtered_prices.values())

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o')
    plt.title(f'Stock Prices for {symbol} for the last {days} days ending {last_refresh}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    symbol = input("Enter the stock symbol (e.g., AAPL, MSFT, etc.): ")
    days = input("Enter the number of days for stock data (default is 30): ")
    try:
        days = int(days)
    except ValueError:
        days = 30  # Default to 30 days if the input is not a valid integer
    
    plot_stock_data(symbol, days)

# main()
if __name__ == '__main__':
    main()
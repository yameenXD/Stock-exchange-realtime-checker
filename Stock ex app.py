import requests

API_KEY = 'JI3DCZJISQY0LHYB'  # Replace this with your actual Alpha Vantage API key
API_URL = "https://www.alphavantage.co/query"

def get_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",  # You can change this depending on the required functionality
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"  # Use "full" for the full-length time series
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extracting just the last day data for simplicity
        last_refresh = data['Meta Data']['3. Last Refreshed']
        last_close = data['Time Series (Daily)'][last_refresh]['4. close']
        return f"Last close price of {symbol} was ${last_close} on {last_refresh}"
    else:
        return "Failed to fetch data. Check your API key and network connection."

def main():
    symbol = input("Enter the stock symbol (e.g., AAPL, MSFT, etc.): ")
    print(get_stock_data(symbol))

if __name__ == '__main__':
    main()
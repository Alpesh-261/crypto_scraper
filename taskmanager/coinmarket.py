import requests
from bs4 import BeautifulSoup
import json

class CoinMarketCap:
    BASE_URL = 'https://coinmarketcap.com/currencies/{}/'

    def fetch_data(self, coin):
        url = self.BASE_URL.format(coin.lower())
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse_data(self, html, coin):
        soup = BeautifulSoup(html, 'html.parser')
        # Example: Scraping price and market cap data
        price = soup.find('div', {'class': 'priceValue'}).text.strip()
        market_cap = soup.find('div', {'class': 'statsValue'}).text.strip()
        return {
            'coin': coin,
            'price': price,
            'market_cap': market_cap,
            # Add more fields as needed
        }

    def get_coin_data(self, coin):
        html = self.fetch_data(coin)
        data = self.parse_data(html, coin)
        return data

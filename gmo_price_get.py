
import requests

def get_gmo_price(symbol):
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/ticker?symbol='+symbol

    response = requests.get(endPoint + path)
    data = response.json()
    price = data["data"][0]
    return price

symbol="BTC"
get_gmo_price(symbol)
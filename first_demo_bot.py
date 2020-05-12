# coding -*- coding: utf-8 -*-

import json
import requests

data_request = requests.get('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=TI6XG302QT0PUZIF')

eur_usd_data = data_request.json()

# last_candle = eur_usd_data["Time Series FX (5min)"]["2020-05-11 20:20:00"]

#esto hace un diccionario con las velas
all_candles = eur_usd_data["Time Series FX (5min)"]

#obtiene una lista con todas las KEY del diccionario con las velas
candles_id = list(all_candles)

print(candles_id[0])
print(candles_id[1])
print(candles_id[2])
print(candles_id[3])
print(candles_id[4])
print(candles_id[5])
print(candles_id[6])

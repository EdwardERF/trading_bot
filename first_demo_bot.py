# coding -*- coding: utf-8 -*-

import json
import requests

data_request = requests.get('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=TI6XG302QT0PUZIF')

eur_usd_data = data_request.json()

# last_candle = eur_usd_data["Time Series FX (5min)"]["2020-05-11 20:20:00"]

# esto hace un diccionario con las velas
all_candles = eur_usd_data["Time Series FX (5min)"]

# obtiene una lista con todas las KEY del diccionario con las velas
candles_id = list(all_candles)

# de esta manera se accede a una ID de la lista
print(candles_id[0])

print('linea para separar')
print('-----------------')
print('Vela numero 1:')

# seleccion de vela por ID
print(all_candles[candles_id[0]])

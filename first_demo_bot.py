# coding -*- coding: utf-8 -*-

import json
import requests
import heapq # para encontrar los highest 2


######################
# VARIABLES GLOBALES #
######################

# variables para pivotes TOP
first_top_pivot = None
second_top_pivot = None

# variables para pivotes BOTTOM
first_bottom_pivot = None
second_bottom_pivot = None

########################
# TERMINO DE VARIABLES #
########################

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

# convertir lista a tupla, para evitar error al llamar h, l, o, c
all_candles_tuple = tuple(all_candles.items())

print('OPEN')
print(all_candles_tuple[0][1]['1. open'])
print('----')
print('HIGH')
print(all_candles_tuple[0][1]['2. high'])
print('----')
print('LOW')
print(all_candles_tuple[0][1]['3. low'])
print('----')
print('CLOSE')
print(all_candles_tuple[0][1]['4. close'])
print('----')

# Encontrar puntos pivote
# Pivotes TOP

# Función que retorna todos los HIGHs en formato diccionario, con keys en numeros
def get_pivot_highs():
  all_highs = { 0: 'initial' }
  all_highs_float = { 0: 0.0000 }

  for i in range(len(all_candles_tuple)): # para cada vela, guardarla en tupla vela: valor
    all_highs[i] = all_candles_tuple[i][1]['2. high']
  
  for i in range(len(all_highs)):
    all_highs_float[i] = float(all_highs[i])

  return all_highs_float

get_pivot_highs()

def get_top_pivots():
  top_pivots = heapq.nlargest(2, get_pivot_highs().values())
  print(get_top_pivots()) # innecesario, solo para efecto visual >> SE PUEDE BORRAR
  return top_pivots

  
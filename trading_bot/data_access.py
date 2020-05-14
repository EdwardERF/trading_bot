# coding -*- coding: utf-8 -*-

import json
import requests
import heapq # para encontrar los highest 2

# obtiene open, high, low, close
def eur_usd_data():
    data_request = requests.get('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=TI6XG302QT0PUZIF')
    eur_usd_data = data_request.json()

    # esto hace un diccionario con las velas
    all_candles = eur_usd_data["Time Series FX (5min)"]
    # pasa datos a formato tuple (mejor manipulacion)
    all_candles_tuple = tuple(all_candles.items())

    # obtiene una lista con todas las KEY del diccionario con las velas
    eur_usd_candles_id = all_candles_tuple

    return eur_usd_candles_id

def actual_candle_data():
    eur_usd = eur_usd_data()
    print('Actual Candle Data:')
    print('OPEN')
    print(eur_usd[0][1]['1. open'])
    print('----')
    print('HIGH')
    print(eur_usd[0][1]['2. high'])
    print('----')
    print('LOW')
    print(eur_usd[0][1]['3. low'])
    print('----')
    print('CLOSE')
    print(eur_usd[0][1]['4. close'])
    print('----')

# Función que retorna todos los HIGHs en formato diccionario, con keys en numeros
def get_pivot_highs(currency):
    all_highs = { 0: 'initial' }
    all_highs_float = { 0: 0.0000 }

    for i in range(len(currency)): # para cada vela, guardarla en tupla vela: valor
        all_highs[i] = currency[i][1]['2. high']
    
    for i in range(len(all_highs)):
        all_highs_float[i] = float(all_highs[i])

    return all_highs_float

# Función que retorna todos los HIGHs en formato diccionario, con keys en numeros
def get_pivot_lows(currency):
  all_lows = { 0: 'initial' }
  all_lows_float = { 0: 0.0000 }

  for i in range(len(currency)): # para cada vela, guardarla en tupla vela: valor
    all_lows[i] = currency[i][1]['3. low']
  
  for i in range(len(all_lows)):
    all_lows_float[i] = float(all_lows[i])

  return all_lows_float

# Función para saber si la vela actual es un pivote top
def is_pivot_top(i, currency):
    #obtencion de 4 pivotes posteriores
    post_four_max = {
        1: get_pivot_highs(currency)[i-1],
        2: get_pivot_highs(currency)[i-2],
        3: get_pivot_highs(currency)[i-3],
        4: get_pivot_highs(currency)[i-4],
    }
    #obtencion de highest pivot de los ultimos 4
    post_max_pivot = max(post_four_max.values())

    #obtencion de 4 pivotes anteriores
    pre_four_max = {
        1: get_pivot_highs(currency)[i+1],
        2: get_pivot_highs(currency)[i+2],
        3: get_pivot_highs(currency)[i+3],
        4: get_pivot_highs(currency)[i+4],
    }
    #obtencion de lower pivot de los ultimos 4
    pre_max_pivot = max(pre_four_max.values())

    current_high = get_pivot_highs(currency)[i]

    if (current_high > pre_max_pivot and current_high > post_max_pivot):
        is_pivot_top = True
    else:
        is_pivot_top = False

    return is_pivot_top

# Función para saber si la vela actual es un pivote bottom
def is_pivot_bottom(i, currency):
  #obtencion de 4 pivotes posteriores
  post_four_bottom = {
    1: get_pivot_lows(currency)[i-1],
    2: get_pivot_lows(currency)[i-2],
    3: get_pivot_lows(currency)[i-3],
    4: get_pivot_lows(currency)[i-4],
  }
  #obtencion de highest pivot de los ultimos 4
  post_bottom_pivot = min(post_four_bottom.values())
  

  #obtencion de 4 pivotes anteriores
  pre_four_bottom = {
    1: get_pivot_lows(currency)[i+1],
    2: get_pivot_lows(currency)[i+2],
    3: get_pivot_lows(currency)[i+3],
    4: get_pivot_lows(currency)[i+4],
  }
  #obtencion de lower pivot de los ultimos 4
  pre_bottom_pivot = min(pre_four_bottom.values())

  current_low = get_pivot_lows(currency)[i]

  if (current_low < pre_bottom_pivot and current_low < post_bottom_pivot):
    is_pivot_bottom = True
  else:
    is_pivot_bottom = False

  return is_pivot_bottom

#obtencion de ultimos dos pivotes top
def get_top_pivots(currency):
  top_pivots_dic = {}
  
  for i in range(len(currency)):
    if (i >= 4):
      if (is_pivot_top(i, currency)):
        if (len(top_pivots_dic) == 0):
          top_pivots_dic[i] = get_pivot_highs(eur_usd)[i]
        elif (len(top_pivots_dic) == 1):
          top_pivots_dic[i] = get_pivot_highs(eur_usd)[i]
          break

  return top_pivots_dic

#obtencion de ultimos dos pivotes bottom
def get_bottom_pivots(currency):
  bottom_pivots_dic = {}
  
  for i in range(len(currency)):
    if (i >= 4):
      if (is_pivot_bottom(i, currency)):
        if (len(bottom_pivots_dic) == 0):
          bottom_pivots_dic[i] = get_pivot_lows(eur_usd)[i]
        elif (len(bottom_pivots_dic) == 1):
          bottom_pivots_dic[i] = get_pivot_lows(eur_usd)[i]
          break

  return bottom_pivots_dic

# FUNCION PARA GENERAR RECTA DE PIVOTES
def calculate_intersection_point(x1, x2, y1, y2, x3):
  m = (y2 - y1) / (x2 - x1)

  intersection_point = m * (x3 - x1) + y1

  return intersection_point

def get_top_intersection_point(currency):
    #esto es: conseguir los valores en formato list para mejor lectura
    top_pivots = list(get_top_pivots(currency).items())
    x1 = top_pivots[0][0]
    y1 = top_pivots[0][1]
    x2 = top_pivots[1][0]
    y2 = top_pivots[1][1]
    x3 = float(currency[0][1]['2. high'])

    intersection_point = calculate_intersection_point(x1, x2, y1, y2, x3)

    return intersection_point

def get_bottom_intersection_point(currency):
    #esto es: conseguir los valores en formato list para mejor lectura
    bottom_pivots = list(get_bottom_pivots(currency).items())
    x1 = bottom_pivots[0][0]
    y1 = bottom_pivots[0][1]
    x2 = bottom_pivots[1][0]
    y2 = bottom_pivots[1][1]
    x3 = float(currency[0][1]['3. low'])

    intersection_point = calculate_intersection_point(x1, x2, y1, y2, x3)

    return intersection_point

# print for testing
eur_usd = eur_usd_data()
print('top pivots')
print(get_top_pivots(eur_usd))
print('bottom pivots')
print(get_bottom_pivots(eur_usd))

print('top intersection point')
print(get_top_intersection_point(eur_usd))

print('bottom intersection point')
print(get_bottom_intersection_point(eur_usd))
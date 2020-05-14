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
print('Vela actual:')
print(candles_id[0])

print('-----------------')

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

# Función que retorna todos los HIGHs en formato diccionario, con keys en numeros
def get_pivot_lows():
  all_lows = { 0: 'initial' }
  all_lows_float = { 0: 0.0000 }

  for i in range(len(all_candles_tuple)): # para cada vela, guardarla en tupla vela: valor
    all_lows[i] = all_candles_tuple[i][1]['3. low']
  
  for i in range(len(all_lows)):
    all_lows_float[i] = float(all_lows[i])

  return all_lows_float

def get_top_highs():
  top_pivots = heapq.nlargest(2, get_pivot_highs().values())
  return top_pivots

def get_top_pivots():
  top_pivots_dic = {}
  
  for i in range(len(get_pivot_highs())):
    if (i >= 4):
      if (es_pivote_top(i)):
        if (len(top_pivots_dic) == 0):
        ## agregar high a la lista
        # top_pivots_list.append(get_pivot_highs()[i])
          top_pivots_dic[1] = get_pivot_highs()[i]
        elif (len(top_pivots_dic) == 1):
          top_pivots_dic[2] = get_pivot_highs()[i]
          break
          ## si lista tiene mas de dos datos, entonces end


  return top_pivots_dic

## FUNCION PARA DETECTAR PIVOTES TOP
def es_pivote_top(i):

  #obtencion de 4 pivotes posteriores
  post_four_max = {
    1: get_pivot_highs()[i-1],
    2: get_pivot_highs()[i-2],
    3: get_pivot_highs()[i-3],
    4: get_pivot_highs()[i-4],
  }
  #obtencion de highest pivot de los ultimos 4
  post_max_pivot = max(post_four_max.values())
  

  #obtencion de 4 pivotes anteriores
  pre_four_max = {
    1: get_pivot_highs()[i+1],
    2: get_pivot_highs()[i+2],
    3: get_pivot_highs()[i+3],
    4: get_pivot_highs()[i+4],
  }
  #obtencion de lower pivot de los ultimos 4
  pre_max_pivot = max(pre_four_max.values())

  current_high = get_pivot_highs()[i]

  if (current_high > pre_max_pivot and current_high > post_max_pivot):
    is_pivot_top = True
  else:
    is_pivot_top = False

  return is_pivot_top

#################################################
## FUNCION PARA DETECTAR PIVOTES BOTTOM // no terminada
def es_pivote_bottom(i):

  #obtencion de 4 pivotes posteriores
  post_four_bottom = {
    1: get_pivot_lows()[i-1],
    2: get_pivot_lows()[i-2],
    3: get_pivot_lows()[i-3],
    4: get_pivot_lows()[i-4],
  }
  #obtencion de highest pivot de los ultimos 4
  post_bottom_pivot = min(post_four_bottom.values())
  

  #obtencion de 4 pivotes anteriores
  pre_four_bottom = {
    1: get_pivot_lows()[i+1],
    2: get_pivot_lows()[i+2],
    3: get_pivot_lows()[i+3],
    4: get_pivot_lows()[i+4],
  }
  #obtencion de lower pivot de los ultimos 4
  pre_bottom_pivot = min(pre_four_bottom.values())

  current_low = get_pivot_lows()[i]

  if (current_low > pre_bottom_pivot and current_low > post_bottom_pivot):
    is_pivot_bottom = True
  else:
    is_pivot_bottom = False

  return is_pivot_bottom


# FUNCION PARA GENERAR RECTA DE PIVOTES
def get_intersection_point(x1, x2, y1, y2, x3):
  m = (y2 - y1) / (x2 - x1)

  intersection_point = m * (x3 - x1) + y1

  return intersection_point

print('Punto de interseccion')
print(get_intersection_point(1, 8, 1.08222, 1.08238, 10))
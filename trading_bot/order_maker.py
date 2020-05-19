import alpaca_trade_api as tradeapi

#authentication and connection details
api_key = 'PK31768SRL9WBTUB3S9F'
api_secret = 'SE1AssOmIUCDXdBdDektImYN0eNzz7YVknY2DrgC'
base_url = 'https://paper-api.alpaca.markets'

#instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

#obtain account information
account = api.get_account()
#print(account)

active_assets = api.list_assets(status='active')

print(active_assets)
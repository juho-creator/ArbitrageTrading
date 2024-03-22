import requests
import json
import locale
from pprint import pprint

# Set the locale for formatting
locale.setlocale(locale.LC_ALL, '')

def upbit():
  url = "https://api.upbit.com/v1/orderbook?markets=KRW-BTC"

  headers = {"accept": "application/json"}
  
  response = requests.get(url, headers=headers)
  
  orderbook = response.text
  orderbook_json = json.loads(orderbook)
  
  btc_orderbook = orderbook_json[0]["orderbook_units"]
  
  
  
  total_ask_volume = 0
  total_bid_volume = 0
  for order in btc_orderbook:
      bid_price = order['bid_price'] 
      ask_price = order['ask_price']
      
      ask_volume = ask_price * order['ask_size']
      bid_volume = bid_price * order['bid_size']
  
      
      total_ask_volume += ask_volume
      total_bid_volume += bid_volume
      
      formatted_ask_volume = locale.format_string("%d", ask_volume, grouping=True)
      formatted_bid_volume = locale.format_string("%d", bid_volume, grouping=True)
      
      # print(f"ask_price : {ask_price}\tbid_price : {bid_price}")
      # print(f"ask_volume : {formatted_ask_volume}")
      # print(f"bid_volume : {formatted_bid_volume}\n")
      
  
  formatted_total_ask_volume = locale.format_string("%d", total_ask_volume, grouping=True)
  formatted_total_bid_volume = locale.format_string("%d", total_bid_volume, grouping=True)
  
  print("UPBIT")
  print(f"total_ask_volume : {formatted_total_ask_volume}")
  print(f"total_bid_volume : {formatted_total_bid_volume}")
  print(f"total_volume : {locale.format_string('%d', total_ask_volume + total_bid_volume, grouping=True)}\n")



def bithumb():
  url = "https://api.bithumb.com/public/orderbook/BTC_KRW"
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers)
  orderbook = response.json()
  
  bids = orderbook["data"]["bids"]
  asks = orderbook["data"]["asks"]
  
  total_bid_volume = sum(float(bid["quantity"]) * float(bid["price"]) for bid in bids)
  total_ask_volume = sum(float(ask["quantity"]) * float(ask["price"]) for ask in asks)
  
  formatted_total_ask_volume = locale.format_string("%d", total_ask_volume, grouping=True)
  formatted_total_bid_volume = locale.format_string("%d", total_bid_volume, grouping=True)
  
  print("BITHUMB")
  print(f"total_ask_volume : {formatted_total_ask_volume}")
  print(f"total_bid_volume : {formatted_total_bid_volume}")
  print(f"total_volume : {locale.format_string('%d', total_ask_volume + total_bid_volume, grouping=True)}\n")



def binance():
    # API endpoint for Binance orderbook
    url = "https://api.binance.com/api/v3/depth?symbol=BTCUSDT"

    # Requesting data from the API
    response = requests.get(url)
    orderbook = response.json()
    pprint(orderbook)    

    # # Extracting bids and asks from the orderbook
    # bids = orderbook["bids"]
    # asks = orderbook["asks"]

    # # Calculating total bid volume
    # total_bid_volume = sum(float(bid[1]) for bid in bids)

    # # Calculating total ask volume
    # total_ask_volume = sum(float(ask[1]) for ask in asks)

    # # Calculating total volume
    # total_volume = total_bid_volume + total_ask_volume

    # # Formatting volume numbers with commas for readability
    # formatted_total_bid_volume = locale.format_string("%d", total_bid_volume, grouping=True)
    # formatted_total_ask_volume = locale.format_string("%d", total_ask_volume, grouping=True)
    # formatted_total_volume = locale.format_string("%d", total_volume, grouping=True)

    # # Printing the volumes
    # print(f"Ask Volume: {formatted_total_ask_volume}")
    # print(f"Bid Volume: {formatted_total_bid_volume}")
    # print(f"Total Volume: {formatted_total_volume}")
    
    
    
    
    

upbit()
bithumb()
binance()
    
    
    
    
    
    
    

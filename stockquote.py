import json
import requests

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": "ORCL,TSLA,MSFT"}

headers = {
    'x-api-key': "0a92eROcca5uq9CMkC2yKaMxlfPiXZl368R11mON"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
#print(response.text)


response.json()
stock_json= response.json()
stockPrice = stock_json['quoteResponse']['result'][0]['regularMarketPrice']
#print(stockPrice)


import sys

def split(input):
    ticker = []
    input = input.split(',')
    
    for x in input:
        ticker.append(x)
    return ticker
    
list = split(sys.argv[1])
names = [x.upper() for x in list]
#print(names)

count = 0
for i in names:
    if i in response.text:
        print(stock_json['quoteResponse']['result'][count]['longName'])
        print(stock_json['quoteResponse']['result'][count]['regularMarketPrice'])
    else:
        print('error')
    count = count+1







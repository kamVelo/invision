import json
import pandas as pd
import requests as rq
import os
from string import ascii_letters
import io
import random

def randomString(length = 6):
    alphas = list(ascii_letters) + list(range(0,10))
    word = ""
    for i in range(0,length):
        word += str(random.choice(alphas))
    return word

def download(symbol:str):
    file_names = ["dset.csv", "rsi.csv"]
    if not os.path.isdir(symbol):
        os.mkdir(symbol)
    else:
        return True
    if len(symbol) == 6: # if its a forex pair
        curr1 = symbol[0:3]
        curr2 = symbol[3:6]
        dset_url = "https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=%s&to_symbol=%s&interval=5min&apikey=%s&datatype=csv&outputsize=full" % (curr1, curr2, randomString(9))
        rsi_url = "https://www.alphavantage.co/query?function=RSI&symbol=%s&interval=5min&time_period=14&series_type=close&apikey=%s&datatype=csv&outputsize=full" % (symbol, randomString(9))



        urls = [dset_url, rsi_url]

    elif len(symbol) <= 5:

        dset_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=5min&apikey=%s&datatype=csv&outputsize=full" % (symbol, randomString(9))
        rsi_url = "https://www.alphavantage.co/query?function=RSI&symbol=%s&interval=5min&time_period=14&series_type=close&apikey=%s&datatype=csv&outputsize=full" % (symbol, randomString(9))
        urls = [dset_url, rsi_url]

    i = 0
    for url in urls:
        response = rq.get(url).content
        file = open(os.path.join(symbol, file_names[i]), "wb")
        file.write(response)
        file.close()
        i += 1
def getFeature(symbol:str):
    price_url = "https://financialmodelingprep.com/api/v3/historical-chart/5min/"+symbol+"?apikey=f5055ef580a960d76b89560fe64d1e33"
    if len(symbol) < 6:# if the symbol is shorter than 6 characters (i.e a stock)
        rsi_url = "https://financialmodelingprep.com/api/v3/technical_indicator/5min/"+symbol+"?period=14&type=rsi&apikey=f5055ef580a960d76b89560fe64d1e33"
        df = pd.read_json(rq.get(rsi_url).content)[["close", "rsi"]].iloc[0:12,:].iloc[::-1]
    elif len(symbol) == 6:
        rsi_url = "https://www.alphavantage.co/query?function=RSI&symbol=%s&interval=5min&time_period=14&series_type=close&apikey=%s&datatype=csv&outputsize=full" % (symbol, randomString(9))
        price_url = "https://financialmodelingprep.com/api/v3/historical-chart/5min/" + symbol + "?apikey=f5055ef580a960d76b89560fe64d1e33"
        df = pd.DataFrame(data=pd.read_json(rq.get(price_url).content)["close"], columns=["close"])
        rsi_df = pd.read_csv(io.StringIO(rq.get(rsi_url).content.decode('utf-8')))["RSI"]
        df["rsi"] = rsi_df
        df = df.iloc[0:12, :].iloc[::-1]
    feature = [[]]
    for item in df.values:
        feature[0].extend(list(item))
    return feature

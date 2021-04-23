import intrinio_sdk as sdk
import requests as rq
import os
import pandas as pd
import numpy as np


def RSI(series, period):
    # gets the difference between each movement
     delta = series.diff().dropna()
     # gets up movements
     u = delta * 0
     #gets down movements
     d = u.copy()
     u[delta > 0] = delta[delta > 0]
     d[delta < 0] = -delta[delta < 0]
     
     
     u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
     u = u.drop(u.index[:(period-1)])
     d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
     d = d.drop(d.index[:(period-1)])
     #gets the rs
     rs = float(pd.Series.ewm(u, com=period-1, adjust=False).mean()) / \
     float(pd.Series.ewm(d, com=period-1, adjust=False).mean())
     #returns RSI
     return 100 - 100 / (1 + rs)
 
    
def getData(symbol):
    data= []
    #list of datapoints required
    values = [ "high_price", "close_price", "volume"]
    #configures the api key
    sdk.ApiClient().configuration.api_key['api_key'] = 'Ojg5YTMwZTNmYzA3Nzc3MTZkNmNkN2I1YzdjZDllODcw'
    secApi = sdk.SecurityApi()
    #for every value in the above list
    for value in values:
        #this gets the value
        response = secApi.get_security_data_point_number(symbol, value)
        #this appends the value to a list of values
        data.append(response)
        
    
    #downloads intraday prices
    
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+symbol+"&interval=5min&apikey=erge&datatype=csv" # url for 5min data used to calculate the sma and rsi
    fileWrite = rq.get(url) #makes http request
    file = os.path.join(symbol, "pricesToUse.csv")#creates csv file to read into dataset
    open(file, "wb").write(fileWrite.content) #writes the response to the csv file
    #read the file to a dataframe variable
    dset = pd.read_csv(os.path.join(symbol, "pricesToUse.csv")) # reads in data to a pandas dataframe
    #gets exclusively the closes for 20 periods
    smaSet = dset.iloc[:20, 4:5].values#gets a set of values for the sma calculation
    #gets the sma by dividing the sum of closes
    sma = float(sum(smaSet)/20)#calculates the sma
    
    #returns the sma for use
    
    rsiSet= dset.iloc[:15, :].iloc[::-1]#gets a set of data for the rsi calculation
    rsiSet = rsiSet["close"] #gets the closes (i.e what we need)
    rsi = RSI(rsiSet, 14)#using calculator.py we get the rsi
    
    """this gets the stochastic just by downloading the latest stochastic data"""
    stochURL = "https://www.alphavantage.co/query?function=STOCH&symbol="+symbol+"&interval=5min&fastkperiod=5&slowkperiod=3&slowdperiod=3&series_type=close&apikey=sdsgsd&datatype=csv&outputsize=full"
    fileWrite = rq.get(stochURL)
    file = os.path.join(symbol, "stochToUse.csv")
    open(file, "wb").write(fileWrite.content)
    #read the file to a dataframe variable
    dset = pd.read_csv(os.path.join(symbol, "stochToUse.csv")).iloc[:, 1:]
    stochastic = dset.iloc[:1, :]
    data.append(sma)
    data.append(stochastic["SlowD"][0])
    data.append(stochastic["SlowK"][0])
    data.append(rsi)
    return data
def getLivePrice(symbol):
    url = "https://financialmodelingprep.com/api/v3/stock/real-time-price/" + symbol.upper()
    response = rq.get(url).json()
    return response["price"]
    
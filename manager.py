#ZENO-AK

import ticker as tick
from makeOrder import makeOrder
from getData import getLivePrice
import time
#opps = screener.screen()
symbol = "AAPL"
#gets the symbol from the screen result

#creates a title with the symbol
print("---------------------%s-------------------------" % symbol)
#instantiates ticker class using the symbol
ticker = tick.ticker(symbol)
#downloads the data for training the predictor (NOT FOR MAKING ACTUAL PREDICTIONS) using the
ticker.getData()
#forms the predictor using the algo class and returns the results of the training/testing phase
pTage, total, totReturn, balance = ticker.train()
#prints the results gathered above 
print("*Percentage success: ", pTage, "%")
print("*Total Profit: %s " % total)
print("*return percentage per 200 5MIN periods: ", totReturn, "%")
print("*balance after 30*200 (approx.) periods: ", balance, "$")
print("                ----------")




#gets the current price using getData.getLivePrice(symbol) which in turn uses an API to get LIVE prices
while True:
    tim = time.ctime()
    hour = int(tim[11:13])
    minute=int(tim[14:16])
    
    if (hour== 14 and minute>30) or (hour>15 and hour<21):
        if minute%5==0:
            price = getLivePrice(symbol)
            prediction=ticker.predict()
            print("We can work this minute!")
            #prints off predicted price 
            print("*Predicted Price: ", prediction, "$")
            print("                ----------")
            print("Actual Price: ", price)
            print("                ----------")
            if prediction > price:
                makeOrder(1, symbol)
            if prediction < price:
                makeOrder(-1, symbol)
    
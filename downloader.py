#ZENO-AK
#DOWNLOADER
import os
import time
import shutil
import requests
import string
import random
class download():
    def __init__(self, symbol):
        #sets the symbol
        self.symbol = symbol.upper()
    def random(self, length=6):
        alphas = list(string.ascii_letters)
        nums = list(str(range(1, 11)))
        alphas += nums
        rd = ""
        for i in range(1, length+1):
            rd += random.choice(alphas)
        return rd
    
    files = ["dset.csv", "sma20.csv", "stoch.csv", "rsi.csv"]
    #constructor gets the symbol of the ticker being downloaded
    

    #def need(self):
        
    
    
    def down(self):
        if os.path.isdir(self.symbol):
            shutil.rmtree(self.symbol)
        os.mkdir(self.symbol)
        try:  
            #url to be downloaded (uses random function above to get a random API key)
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+self.symbol+"&interval=5min&apikey="+self.random()+"&datatype=csv&outputsize=full"
            #creates a read of the url(CSV)
            myfile = requests.get(url)
            #writes the read to a csv file
            file = open(os.path.join(self.symbol, "dset.csv"), 'wb')
            file.write(myfile.content)
            file.close()
            time.sleep(15)
            #url to be downloaded (uses random function above to get a random API key)
            url = "https://www.alphavantage.co/query?function=SMA&symbol="+self.symbol+"&interval=5min&time_period=20&series_type=close&apikey="+self.random()+"&datatype=csv&outputsize=full"
            #creates a read of the url(CSV)
            myfile = requests.get(url)
            #writes the read to a csv file
            file = open(os.path.join(self.symbol, "sma20.csv"), 'wb')
            file.write(myfile.content)
            file.close()
            time.sleep(15)
            
            
            #url to be downloaded (uses random function above to get a random API key)
            url = "https://www.alphavantage.co/query?function=STOCH&symbol="+self.symbol+"&interval=5min&fastkperiod=5&slowkperiod=3&slowdperiod=3&series_type=close&apikey=" +self.random() + "&datatype=csv&outputsize=full"
            #creates a read of the url(CSV)
            myfile = requests.get(url)
            #writes the read to a csv file
            file = open(os.path.join(self.symbol, "stoch.csv"), 'wb')
            file.write(myfile.content)
            file.close()
            time.sleep(15)
            
            #url to be downloaded (uses random function above to get a random API key)
            url = "https://www.alphavantage.co/query?function=RSI&symbol="+self.symbol+"&interval=5min&time_period=14&series_type=close&apikey=" +self.random() + "&datatype=csv&outputsize=full"
            #creates a read of the url(CSV)
            myfile = requests.get(url)
            #writes the read to a csv file
            file = open(os.path.join(self.symbol, "rsi.csv"), 'wb')
            file.write(myfile.content)
            file.close()
            time.sleep(15)
           
            
            
        except:
            print("No Internet connection. Connect to the Internet before launching again.")
            shutil.rmtree(self.symbol)

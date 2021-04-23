#ZENO-AK

from downloader import download
from algorithm import algo



class ticker():
    #constructor, self.ticker is the ticker variable used by the class (opp)
    #ticker is the variable of the ticker passed in the constructor
    def __init__(self, symbol):
        #sets the variable
        self.symbol = symbol
        
        
    #uses the downloader script to download data necessary for training the model (NOT TESTING)
    def getData(self):
        #this instantiates the downloader class
        downloader = download(self.symbol)
        #uses the instantiated class's method
        downloader.down()
    
    #trains the predictor and creates a variable out of it for future use
    def train(self):
        self.predictor = algo(self.symbol)
        pTage, total, totReturn, balance = self.predictor.polyReg()
        return pTage, total, totReturn, balance
        
    #uses the predictor created above to get a specific prediction
    def predict(self):
        #gets the prediction
        prediction = self.predictor.analyse()    
        #returns the prediction
        return prediction
        
    

    
   




        
    
    
    
    
    

        
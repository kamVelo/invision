#ZENO-AK
import pandas as pd
import numpy as np
import os
import getData


class algor:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
    def polyReg(self):
        #gets the dataset from file and removes time index and reverses it
        dataset = pd.read_csv(os.path.join(self.symbol, "dset.csv")).iloc[:, 1:].iloc[::-1]
        #creates a new index from 1 - x instead of x -1 (i.e going down)
        dataset.index = pd.RangeIndex(start = 0, stop=len(dataset), step = 1)
        
        #gets the sma 20 from file and removes time index and reverses it
        sma20 = pd.read_csv(os.path.join(self.symbol, "sma20.csv")).iloc[:,1:].iloc[::-1]
        #creates new 'proper' index 
        sma20.index = pd.RangeIndex(start = 0, stop = len(sma20), step = 1)
        #names it "SMA 20"
        sma20.columns = ["SMA 20"]
        
        #gets the triple exponential moving average from file and removes time index and reverses it
        stoch = pd.read_csv(os.path.join(self.symbol, "stoch.csv")).iloc[:,1:].iloc[::-1]
        #creates new 'proper' index 
        stoch.index = pd.RangeIndex(start = 0, stop = len(stoch), step = 1)
        #names it "t3"
        stoch.columns = ["slowK", "slowD"]
        
        #gets the triple exponential moving average from file and removes time index and reverses it
        rsi = pd.read_csv(os.path.join(self.symbol, "rsi.csv")).iloc[:,1:].iloc[::-1]
        #creates new 'proper' index 
        rsi.index = pd.RangeIndex(start = 0, stop = len(rsi), step = 1)
        #names it "t3"
        rsi.columns = ["rsi"]


        
        
        #gets the open column from dataset and converts to numpy array
        opens = dataset["open"].values
        #adds a NaN value to the bottom
        opens = np.append(opens, np.NaN)
        #deletes top value to virtually shift each open up(i.e making it the 'future open')
        opens = np.delete(opens, 0, axis = 0)
        #converts it to a dataframe so its easier to append to the dataset and other things 
        opens = pd.DataFrame(opens)
        #names the column future opens for ease of identification
        opens.columns = {"Future Opens"}
        
        #gets the open column from dataset and converts to numpy array
        closes = dataset["close"].values
        #adds a NaN value to the bottom
        closes = np.append(closes, np.NaN)
        #deletes top value to virtually shift each open up(i.e making it the 'future open')
        closes = np.delete(closes, 0, axis = 0)
        #converts it to a dataframe so its easier to append to the dataset and other things 
        closes = pd.DataFrame(closes)
        #names the column future opens for ease of identification
        closes.columns = {"Future Closes"}
        
        #creates complete dataset by appending all data together
        dataset = pd.concat([dataset, sma20, stoch,rsi, opens,closes], axis = 1)
        
        #lens is a list containing all the lengths of the various datasets
        lens = [len(dataset), len(sma20), len(closes), len(opens), len(stoch), len(rsi)]
        #idx is the lowest index of the dataframes 
        idx = min(lens) - 1
        
        #this shortens the dataset to the lowest index so that there are no null values
        dataset = dataset.iloc[:][:idx]
        #get rid of bottom row in case the NaN from previously is still there
        #dataset.drop(len(dataset) - 1)
        del dataset["low"]
        del dataset["open"]
        returnable = dataset
        #X is the data uses to make predictions
        X =dataset.iloc[:, :-1].values
        #Y is the data used to train and test predictions
        Y = dataset["Future Closes"].values
        
        #splits data into a training and a test dataset
        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
        
        #scales the data so that drastic price moves dont affect the data results
        from sklearn.preprocessing import StandardScaler
        self.sc_X = StandardScaler()
        self.test_xTest = x_test
        self.test_xTrain = x_train
        x_train = self.sc_X.fit_transform(x_train[:, :-1])
        x_test = self.sc_X.transform(x_test[:, :-1])
        self.sc_y = StandardScaler()
        y_train = self.sc_y.fit_transform(y_train.reshape(-1, 1))
        y_test = self.sc_y.transform(y_test.reshape(-1, 1))
        
        
        ##fits a polynomial regressor to the data
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import PolynomialFeatures
        #fits polynomial features to the data
        self.poly_reg = PolynomialFeatures(degree = 1)
        X_poly_train = self.poly_reg.fit_transform(x_train)
        
        
        #fit the linear regressor to the training set
        self.lin_reg_2 = LinearRegression()
        self.lin_reg_2.fit(X_poly_train, y_train)
        
        #polynomial-ises the test set
        X_poly_test= self.poly_reg.fit_transform(x_test) 
        """_________________________________________________________________"""
        #predicts
        y_pred = self.lin_reg_2.predict(X_poly_test)
        
        #creates the dataframe for checking results
        fullTest = pd.DataFrame(self.test_xTest)
        
        fullTest = fullTest.iloc[:, 7:]
        #returnable = fullTest
        #return returnable
        fullTest.columns = ["Opens"]
        
        #adds the closes and predictions to the test
        fullTest["Closes"] = self.sc_y.inverse_transform(y_test)
        fullTest["Predictions"]= self.sc_y.inverse_transform(y_pred)
        
        #number of correct predictions
        correctPredictions = 0
        #number of incorrect predictions
        incorrectPredictions = 0
        #profit (without subtracting loss)
        profit = 0
        #loss (regardless of profit)
        loss = 0
        #price of the stock by the end
        price = 0
        
        #for every index and row in the full test
        for index, row in fullTest.iterrows():
            #open is the 'future open' from the original dataset
            Open = row["Opens"]
            #close is the 'future close' from the original dataset
            Close = row["Closes"]
            #prediction is the y_pred
            Prediction = row["Predictions"]
            
            #this is the difference between the open and close (no prediction)
            actualDif= float(Open) - float(Close)
            
            #this is the difference between the open and the prediction
            predDif = float(Open) - float(Prediction)
            
            #if the directions of the predicted and real movement align :
            if (actualDif > 0 and predDif > 0) or (actualDif < 0 and predDif < 0 ):
                #increase correct predictions by 1
                correctPredictions += 1
                
                #add the profit made by the individual movement
                profit+= abs(actualDif)
            #if the predicition is incorrect or there is no movement
            else:
                #increase the incorrect predictions by 1
                incorrectPredictions += 1
                #increase the loss by the movement
                loss += abs(actualDif)
            #sets the price for future calculations
            price = Close
        #percentage of correctPredctions to the possible correct predictions
        pTage = round((correctPredictions/(len(fullTest)-1)*100), 2)
        #prints the percentage
        
        
        #number of shares buy-able using a balance of 600$
        shares = round(12500/price)
        #gets the profit(on-its-own)
        profit *= shares
        #gets the loss(on-its-own)
        loss *= shares
        
        #gets the EOD P/L
        total = profit - loss
        #gets the total return over the day
        ret = total / 25000
        #gets the return as a percentage
        totReturn = ret*100
        #adds 1 so it can be used for compound interest calculations
        ret += 1
        #calculates a predicted balance given a constant daily return over thirty days
        balance = 25000*ret**30
        #returns the results created above.
        return pTage, total, totReturn, balance
        
        
        
        
    def analyse(self):
        #gets the data from getData.py
        vals = getData.getData(self.symbol)
        
        vals = np.array(vals).reshape(1, -1)
        
        scaledVals = vals
        #
        scaledVals = self.sc_X.transform(vals)
        # returns the values
        polyScaledVals = self.poly_reg.transform(scaledVals)
        pred = self.lin_reg_2.predict(polyScaledVals)
        pred = self.sc_y.inverse_transform(pred)
        
        
        return pred[0][0]
        
        

        

        
    
        
        
        
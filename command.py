from time import sleep
from datetime import datetime as dt
from trader import Trader
import os
from download import download, getFeature
from string import punctuation as special_chars
from classifier import Classifier
from positionManager import PositionManager
from longPosition import LongPosition as Long
from shortPosition import ShortPosition as Short
from order import Order
import requests as rq
from selenium.common.exceptions import NoSuchWindowException
class command:
    def __init__(self, symbol):

        # validation routine for the symbol entered
        self.symbol = symbol.upper()
        if len(symbol) > 6 or any(spec in self.symbol for spec in special_chars):
            print(f"Sorry, your ticker: {self.symbol} is longer than 6 characters long and thus invalid please re-enter the ticker and try again.")
            exit(-1)
            #exits the program if the symbol is invalid.

        # checks to see if data is downloaded, if it isn't then download some
        elif not os.path.isdir(self.symbol):
            print("No data downloaded for this symbol.\n Downloading now...")
            download(self.symbol)

        # gets the classifier and initialises it.
        self.quant = Classifier(self.symbol)
        self.quant.prepNN()

        #gets the trader and starts it up
        self.trader = Trader(self.symbol)

        #gets starting balance for the session:
        self.init_bal = 0
        while self.init_bal == 0:
            self.init_bal = self.trader.getBalance()

        #declaring and initialising core variables
        self.feature = [[]] #feature matrix which will be used but is empty until it is gradually filled over an hour
        self.position = None
        self.pos_manager = PositionManager(self.symbol)

        #getting url based on whether or not it is a
        #starts up the operation
        self.run()
    def run(self):
        """
        this function is what brings together all the operations.
        it will act as the user interface and provide all information to the user.

        :return:
        """


        #anncounces that trader is starting
        print("*--------------------------------------------------------------*")
        print("*----------------------- VERY IMPORTANT -----------------------*")
        print("*--------------------------------------------------------------*")

        print(f"*                          {dt.today()}          *")
        print("*                        STARTING TRADER                       *")
        print("*--------------------------------------------------------------*")


        min = dt.today().minute
        sec = dt.today().second

        #run this loop theoretically forever
        goForTrade = True # this variable allows the trader to make a trade, it is reset to false after a trade has been made to prevent the trader from running twice or more in the same minute
        goForBal = True
        goForCheck = True
        while True:
            disallow = False
            self.cur_bal = self.trader.getBalance()
            if min % 5 == 0 and goForBal and self.cur_bal!=None:
                print(f"\t\tCurrent Balance: {self.cur_bal} - Initial Balance: {self.init_bal} - Growth: {round((self.cur_bal/self.init_bal*100)-100, 2)}%")
                goForBal = False
            elif min%5!= 0:
                goForBal = True
            try:
                if self.cur_bal/self.init_bal <= 0.85:
                    print("*--------------------------------------------------------------*")
                    print("*----------------------- VERY IMPORTANT -----------------------*")
                    print("*--------------------------------------------------------------*")
                    print("Balance has fallen too far. Closing trader and all open position(s)")
                    print("*                          -------------                       *")

                    if self.position:
                        closed = self.position.close()
                        if closed == False:
                            print("*--------------------------------------------------------------*")
                            print("*----------------------- VERY IMPORTANT -----------------------*")
                            print("*--------------------------------------------------------------*")
                            print("Position could not be closed. Major error. closing trader without further action. Please manually check the trading dashboard.")
                            exit(-1)
                        else:
                            self.pos_manager.record(self.position)
            except ZeroDivisionError and TypeError:
                pass

            if min==0 and goForTrade:
                # every hour
                try:
                    self.feature = getFeature(self.symbol) #fills the feature using the getFeature function in download.py
                    self.pred = self.quant.predict(self.feature)  # makes prediction using prediction matrix just created above
                except rq.exceptions.SSLError:
                    print("Error - No Data Available")
                    self.pred = None
                try:
                    print(f"\t{dt.today()} - Prediction: {self.pred.name} | Current Position: {self.position.direction.name}") #prints out: time - Prediction: LONG/SHORT | Current Position: LONG/SHORT
                except AttributeError:
                    print(f"\t{dt.today()} - Prediction: {self.pred.name} ")
                lastPos = self.pos_manager.getLastPosition() #gets the last position recorded

                if lastPos:
                    if lastPos.direction == self.pred and lastPos.status == "LOSS": # if the last position recorded was in the same direction as this one and was a loss then disallow this trade.
                        print("\t You must wait at least another period (1 hour) to open this position as the previous iteration of this position was a loss")
                        disallow = True
                #if there is already an open position
                if self.position:
                    #if the position is open in the same direction
                    if self.position.direction == self.pred:
                        print("\t\tPrediction in the same direction as the current position. Maintaining current position")
                    #if it is open in an opposite direction
                    else:
                        #close the current position and record it
                        self.position.close()
                        self.pos_manager.record(self.position)
                        self.position = None
                        #open new position
                        if self.pred:

                            self.position = (Long(self.trader), Short(self.trader))[self.pred == Order.SHORT]
                            self.position.open(disallow)
                            print("-----------Position Information-----------------")
                            print(f"{dt.today()} - {self.position.direction.name} {self.position.quantity} @ {self.position.open_price}")
                #if no position is open
                else:
                    #open new position
                    self.position = (Long(self.trader), Short(self.trader))[self.pred == Order.SHORT]
                    self.position.open(disallow)
                sleep(3)
                goForTrade = False
            elif min % 1 == 0 and goForCheck and min != 0 and sec == 0:

                if self.position:
                    print(f"{dt.today()} - Current P/L: {self.position.getProfit()} - Peak P/L: {self.position.peak} - Margin: {self.position.getMargin()}")
                    closed, msg = self.position.check()
                    if closed:
                        self.pos_manager.record(self.position)
                        self.position=None

                    print(msg)
                goForCheck = False
            elif sec!=0:
                goForCheck=True
            elif min != 0:
                goForTrade = True

            min = dt.today().minute
            sec = dt.today().second
try:
    c = command("AAPL")
except NoSuchWindowException:
    print("Exiting trader.")

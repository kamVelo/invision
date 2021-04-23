#ZENO-AK
#this is an attempt at using the tws api from python:
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.common import *
from ibapi.order_state import OrderState
from getData import getLivePrice
from getBalance import getBalance
from getPosition import getPosition

#creates an app as an interface between EWrapper and EClient
class app(EWrapper, EClient):
    #constructor takes the action (i.e BUY or SELL), the stock (i.e AAPL) and the quantity (i.e 10 shares)
    def __init__(self, action:int, stock:str, quantity:str):
        EClient.__init__(self, self)
        self._action = ("SELL", "BUY")[action*-1 == -1]#an input parameter -1 means sell input 1 means buy
        self.stock = stock
        self.quantity = quantity
        
        
    #gets the next order id and by extension orders the stock placed using the method below
    def nextValidId(self, orderId:int):
        self.nextOrderId = orderId
        self.order(self._action, self.quantity, self.stock)
        self.end()
        
        
    def order(self, action, quantity, stock):
        #instantiates the contract object
        contract = Contract()
        #sets the symbol
        contract.symbol = stock.upper()
        #sets the obligatory info
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "ISLAND"
        #instantiates order object
        order = Order()
        #sets the action
        order.action = action.upper()
        #market order type for quicker execution
        order.orderType = "MKT"
        #sets the quantity
        order.totalQuantity = quantity
        #actually places the order
        self.placeOrder(self.nextOrderId, contract, order)
        
    
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        if errorCode != 2106 and errorCode != 2104:
            print("ERROR %s %s %s" % (reqId, errorCode, errorString))
    
    #ends the app
    def end(self):
        #done (i.e its finished doing its job)
        self.done = True
        #disconnects from the tws API so the same socket can be used again later
        self.disconnect()

def makeOrder(action:int, symbol:str):
    position = getPosition(symbol.upper())
    
    price = getLivePrice(symbol)
    balance = getBalance()/4
    quantity = (round(balance/price,0)-abs(position), (round(balance/price, 0))+abs(position))[(action*-1>0 and position*-1<0) or (action*-1<0 and position*-1>0)]
    order = app(action, symbol.upper(), quantity)
    order.connect("127.0.0.1", 7496, 999)
    order.startApi()
    order.run()
    

    



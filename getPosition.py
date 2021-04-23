#ZENO-AK
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
import time
from ibapi.common import *
from threading import Thread


class app(EClient, EWrapper):
    def __init__(self, symbol):
        EClient.__init__(self, self)
        self.symbol = symbol
        self.positions = 0
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        if errorCode != 2106 and errorCode != 2104:
            print("ERROR %s %s %s" % (reqId, errorCode, errorString))
        
    def nextValidId(self, orderId:int):
        self.nextOrderId = orderId
        self.reqPositions()
        time.sleep(0.01)
        self.end()
        
    def position(self, account: str, contract: Contract, position: float,avgCost: float):
        super().position(account, contract, position, avgCost)
        self.positions = position
        
    def positionEnd(self):
        pass
    
    def end(self):
        
        self.done = True
        self.disconnect()
        
        
def getPosition(symbol):
    getPos = app(symbol)
    getPos.connect("127.0.0.1", 7496, 998)
    getPos.startApi
    getPos.run()
    return getPos.positions

#ZENO-AK
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
import time
from ibapi.common import *

class app(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        
        
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        if errorCode != 2106 and errorCode != 2104:
            print("ERROR %s %s %s" % (reqId, errorCode, errorString))
        
    def nextValidId(self, orderId:int):
        self.nextOrderId = orderId
        self.reqAccountSummary(1, "All", "TotalCashValue")
        
        
        
    def accountSummary(self, reqId:int, account:str, tag:str, value:str,currency:str):
        super().accountSummary(reqId, account, tag, value, currency)
        self.value = value
        
        
    def accountSummaryEnd(self, reqId:int):
        super().accountSummaryEnd(reqId)
        self.end()
    
    def end(self):
        self.done = True
        self.disconnect()
    
def getBalance(): 
    getBal = app()
    getBal.connect("127.0.0.1", 7496, 997)
    getBal.startApi()
    getBal.run()
    return float(getBal.value)

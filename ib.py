from ibapi.common import TickerId, TickAttrib
from ibapi.ticktype import TickType
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
import logging
from time import sleep
from threading import Thread
import atexit
from position import Position
from shortPosition import ShortPosition
from longPosition import LongPosition
from yahoo_fin.stock_info import get_live_price
class IB(EClient,EWrapper):
    def __init__(self):
        self.pnlReqId = 1
        self.profit_requested = None
        self.positionReceived = False
        self.orderMade = False
        self.raw_pos = []
        # necessary instantiations per IBAPI documentation
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        # connects app to TWS
        self.connect("127.0.0.1", 7497, 999)

        # creates and starts EReader thread
        run = Thread(target=self.run, daemon=True)
        run.start()

        # ensures that app always disconnects cleanly
        atexit.register(self.end)

    def nextValidId(self, orderId: int):
        """
        EWrapper function to receive the new order id and set member variable
        :param orderId: next orderId received from TWS
        :return: None
        """

        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId

    def error(self, reqId:int, errorCode:int, errorString:str):
        """

        :param reqId: error id (-1 indicates notification not error)
        :param errorCode: error code string
        :param errorString: the actual error description
        :return:
        """
        if reqId != -1: # i.e if not a notification
            print(f"ERROR:: Code:{errorCode} - {errorString}")

    def order(self, instrument, direction, quantity):
        """
        function to allow market orders to be created and placed
        :param instrument: the instrument's symbol
        :param direction: i.e BUY or SELL
        :param quantity: number of shares
        :return: True/False for order PLACED (not necessarily successful just placed)
        """
        contract = Contract()
        symbol = instrument
        if len(instrument) == 6: # if it is a forex pair
            sec_type = "CASH"
            symbol = instrument.upper()[0:3]
            currency = instrument.upper()[3:6]

            exchange = "IDEALPRO"
        elif len(instrument) <= 5: # if it is a stock
            sec_type = "STK"
            currency = "USD"
            contract.primaryExchange = "ISLAND"
            exchange = "SMART"
        else: # if it is neither stock or forex pair refuse to place order, return False for failed order.
            return False
        # creates Contract object and fills necessary data

        contract.symbol = symbol
        contract.secType = sec_type
        contract.currency = currency
        contract.exchange = exchange

        # creates order and fills out details
        order = Order()
        order.action = direction.upper()
        order.orderType = "MKT"
        order.totalQuantity = quantity
        # gets latest order id
        old_val = self.nextValidOrderId
        self.reqIds(-1)
        while self.nextValidOrderId == old_val and self.orderMade:  # waits until order id updated.
            pass
        # places the order and returns True since no errors would have been raised by this point.
        self.placeOrder(self.nextValidOrderId, contract, order)
        self.orderMade = True
        pos = (ShortPosition(self), LongPosition(self))[direction=="BUY"]

        return True

    def accountSummary(self, reqId:int, account:str, tag:str, value:str,currency:str):
        """
        receives the account summary from TWS
        :param reqId: id supplied by reqAccountSummary
        :param account: if multiple accounts then the account selected
        :param tag: tag requested by EClient
        :param value: value returned from request
        :param currency: currency that value is in.
        :return: None
        """
        if tag == "AvailableFunds": # for getBalance
            self.balance = float(value)
    def accountSummaryEnd(self, reqId:int):
        self.accountSummaryReceived = True

    def getBalance(self):
        """
        gets the available funds for trading from TWS
        :return: float balance of available funds in account for trading
        """
        self.accountSummaryReceived = False
        self.reqAccountSummary(-1, "All","AvailableFunds")
        while not self.accountSummaryReceived: # waits until account summary received to return value
            pass
        return self.balance

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        """
        EWrapper method. called when EClient.reqPositions() or when position opened.
        :param account: account order made with
        :param contract: contract of this position
        :param position: number of shares
        :param avgCost: cost trade made at
        :return: None
        """
        pos = {}
        if contract.secType == 'STK':
            inst_symbol = contract.symbol
        elif contract.secType == 'CASH':
            inst_symbol = contract.symbol+contract.currency
        pos["symbol"] = inst_symbol
        pos["contract"] = contract
        pos["no. shares"] = position
        pos["open prices"] = avgCost
        pos["margin"] = avgCost * position

        self.raw_pos.append(pos)
    def positionEnd(self):
        """
        called when all the position information has been sent.
        :return: None
        """
        print("RECEIVED")
        self.positionReceived = True

    def getMargin(self, symbol):
        """
        function to get the margin of any given position using EClient.reqPositions()
        :param symbol: symbol of the stock whose margin is being requested
        :return: float margin of the stock.
        """
        self.raw_pos = []
        self.positionReceived = False
        self.reqPositions() # use eclient method to get position info.
        while not self.positionReceived: # waits for the position information to be fully received using positionEnd()
            pass
        for pos in self.raw_pos:
            if pos["symbol"] == symbol:
                return pos["margin"] # if the position is found return this.
        return None # if no position is found None will be returned

    def getPrice(self,symbol):
        """
        gets the price of ticker specified.
        just uses yahoo_fin library because its simpler + quicker than using ibapi.
        :param symbol: symbol for the data to be retrieved.
        :return: Float - current price.
        """
        return get_live_price(symbol)


    def pnlSingle(self, reqId: int, pos: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        self.profit_requested = dailyPnL # this variable will contain the profit requested most recently.

    def getProfit(self,symbol):
        self.raw_pos = []
        self.reqPositions()
        while len(self.raw_pos) == 0:
            pass
        for pos in self.raw_pos:
            if pos["symbol"] == symbol:
                id = pos["contract"].conId
                self.profit_requested = None
                self.reqPnLSingle(self.pnlReqId, "DU3919760", "", id)
                while self.profit_requested == None:
                    pass
                self.cancelPnLSingle(self.pnlReqId)
                self.pnlReqId += 1
                return self.profit_requested
    def end(self):
        print("TRADER DISCONNECTING")
        self.done = True
        self.disconnect()
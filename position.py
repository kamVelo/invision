"""
this is a template class for all position types
"""
from datetime import datetime as dt
import pandas as pd
import requests
import finnhub
class Position:
    def __init__(self,symbol,direction, trader):
        self.finnhub_client = finnhub.Client(api_key="c4hsvkiad3ifj3t4ktf0")
        self.direction = direction
        self.posId = None
        self.trader = trader
        self.opened = False
        self.disallowed = False
        self.open_price = None
        self.shares = None
        self.margin = None
        self.close_price = None
        self.pl = None
        self.close_time = None
        self.peak = None
        self.symbol = symbol
        self.profit_discount = None
    def open(self, disallow=False):
        # by default disallow to false.
        # if disallowed then set disallow to true.
        # if not disallow then open position
        if disallow: self.disallow = disallow
        elif self.direction != None: return self.trader.order(self.symbol, self.direction)
    def close(self):
        if self.opened:
            try:
                self.close_price = self.trader.getPrice(self.symbol)
            except requests.exceptions.SSLError:
                self.close_price = "NA"
            self.pl = self.trader.getProfit(self)
            self.closed = self.trader.closePosition(self)
        else:
            self.closed = None
            self.close_time = None
        return self.closed
    def getPrice(self):
        return self.finnhub_client.quote(self.symbol)["c"]
    def check(self):
        profit = self.getProfit()
        self.margin = self.getMargin()
        closed = None
        if not profit or not self.margin:
            msg = "Data Error"
            return closed,msg
        if self.peak == None: self.peak = profit
        elif profit>self.peak:
            self.peak = profit
        if profit/self.margin <=-0.03:
            msg = "\t\tUnrealised Loss is too great. Closing position."
            closed = self.close()
        elif profit/self.margin >= 0.1:
            msg = "\t\tProfit has exceeded 10% of margin. Closing position; securing profit."
            closed = self.close()
        elif profit/self.peak <= 0.85 and self.peak/self.margin >= 0.025: # if profit is less than 15% of peak and the peak has exceeded 2.5% of the total self.margin
            msg = "\t\tProfit has descended from peak by more than 10% closing position."
            closed = self.close()
        else:
            msg = "\t\tNo issues with the position."
        return closed, msg

    def getProfit(self):
        return self.trader.getProfit(self)
    def getMargin(self):
        return self.trader.getMargin(self.symbol)


def posFromSeries(row:pd.Series):
    if not row:
        close_time = row["timestamp"]
        direction = row["position"]
        close_price = row["close price"]
        open_price = row["open price"]
        pl = row["P/L"]
        status = row["status"]
        quantity = row["quantity"]
        return OldPosition(direction, close_time, open_price, close_price,pl, status, quantity)
    else:
        return None
class OldPosition:
    def __init__(self, direction=None, close_time=None, open_price=None, close_price=None, pl=None, status=None, quantity=None):
        self.direction = direction
        self.close_time = close_time
        self.open_price = open_price
        self.close_price = close_price
        self.pl = pl
        self.status = status
        self.quantity = quantity


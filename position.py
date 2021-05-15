"""
this is a template class for all position types
"""
from t212executor import Executor
from datetime import datetime as dt
import pandas as pd
class Position:
    def __init__(self, direction, trader:Executor):
        self.direction = direction
        self.trader = trader
        self.opened = False
        self.disallowed = False
        self.open_price =  None
        self.close_price = None
        self.pl = None
        self.close_time = None
        self.quantity = None
        self.peak = None
    def close(self):
        self.close_price = self.trader.getCurrentPrice()
        self.pl = self.trader.getProfit()
        if self.opened:
            self.closed = self.trader.closeOrder()
        else:
            self.closed = None
        self.close_time = dt.today()
        return self.closed

    def check(self):
        profit = self.getProfit()
        margin = self.getMargin()
        closed = None
        if not profit or not margin:
            msg = "Data Error"
            return closed,msg
        if self.peak == None: self.peak = profit
        elif profit>self.peak:
            self.peak = profit
        if profit/margin <=-0.05:
            msg = "\t\tUnrealised Loss is too great. Closing position."
            closed = self.close()
        elif profit/margin >= 0.1:
            msg = "\t\tProfit has exceeded 10% of margin. Closing position; securing profit."
            closed = self.close()
        elif profit/self.peak <= 0.85 and self.peak/margin >= 0.025: # if profit is less than 15% of peak and the peak has exceeded 2.5% of the total margin
            msg = "\t\tProfit has descended from peak by more than 10% closing position."
            closed = self.close()
        else:
            msg = "\t\tNo issues with the position."
        return closed, msg

    def getProfit(self):
        return self.trader.getProfit()
    def getMargin(self):
        return self.trader.getMargin()


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


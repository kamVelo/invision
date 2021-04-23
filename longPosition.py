#imports
from position import Position
from trader import Trader
from order import Order



"""this class inherits from the position class as a long position"""
class LongPosition(Position):
    def __init__(self, trader:Trader):
        super().__init__(Order.LONG, trader)

    def open(self, disallowed=False):
        if not disallowed:
            self.trader.buyOrder()
            self.open_price = self.trader.getOpenPrice()
            self.quantity = self.trader.getQuantity()
            self.opened = True
        self.disallowed = disallowed
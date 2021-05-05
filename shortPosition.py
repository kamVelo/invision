from t212executor import executor
from order import Order
from position import Position

class ShortPosition(Position):
    def __init__(self, trader:executor):
        super().__init__(Order.SHORT, trader)

    def open(self, disallowed=False):

        if not disallowed:
            self.trader.sellOrder()
            self.open_price = self.trader.getOpenPrice()
            self.quantity = self.trader.getQuantity()
            self.opened = True
        self.disallowed = disallowed
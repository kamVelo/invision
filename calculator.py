#ZENO-AK
import numpy as np

import pandas as pd

# this function returns the RSI

def RSI(series, period):
    # gets the difference between each movement
     delta = series.diff().dropna()
     # gets up movements
     u = delta * 0
     #gets down movements
     d = u.copy()
     u[delta > 0] = delta[delta > 0]
     d[delta < 0] = -delta[delta < 0]
     
     
     u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
     u = u.drop(u.index[:(period-1)])
     d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
     d = d.drop(d.index[:(period-1)])
     #gets the rs
     rs = float(pd.Series.ewm(u, com=period-1, adjust=False).mean()) / \
     float(pd.Series.ewm(d, com=period-1, adjust=False).mean())
     #returns RSI
     return 100 - 100 / (1 + rs)








    




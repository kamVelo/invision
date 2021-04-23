import pandas as pd
import requests as rq
import json
url = "https://financialmodelingprep.com/api/v3/historical-chart/5min/AAPL?apikey=f5055ef580a960d76b89560fe64d1e33"
response = rq.get(url).content
jre = json.loads(response)
df = pd.read_json(response)
print(df)
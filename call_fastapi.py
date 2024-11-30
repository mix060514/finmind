import requests
import pandas as pd 

payload = dict(
    stock_id = '0050',
    start_date = '20240101',
    end_date = '20240131',
)

res = requests.get('http://127.0.0.1:8888/taiwan_stock_price', params=payload)
print(res)
df = pd.DataFrame(res.json()['data'])
print(df)

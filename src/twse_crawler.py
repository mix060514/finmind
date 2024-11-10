import datetime
import sys
import typing
import time

import pandas as pd
import requests 
from loguru import logger
from pydantic import BaseModel


def gen_date_list(start_date: str, end_date: str) -> typing.List[str]:
    start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    date_list = []
    while start_date <= end_date:
        date_str = start_date.strftime('%Y%m%d')
        date_list.append(date_str)
        start_date += datetime.timedelta(days=1)
    return date_list

def twse_header() -> dict:
    return {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6,ja;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=0F737D9CC8336CCBF766A599DAD28B0F',
        'DNT': '1',
        'Host': 'www.twse.com.tw',
        'Referer': 'https://www.twse.com.tw/zh/trading/historical/mi-index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

def colname_zh2en(df: pd.DataFrame, colname) -> pd.DataFrame:
    taiwan_stock_price = {
        '證券代號': 'stock_id',
        '證券名稱': '',
        '成交股數': 'trade_volume',
        '成交筆數': 'transactions',
        '成交金額': 'trade_value',
        '開盤價': 'open',
        '最高價': 'max',
        '最低價': 'min',
        '收盤價': 'close',
        '漲跌(+/-)': 'dir',
        '漲跌價差': 'change',
        '最後揭示買價': '',
        '最後揭示買量': '',
        '最後揭示賣價': '',
        '最後揭示賣量': '',
        '本益比': ''
    }
    df = df.rename(columns=taiwan_stock_price).drop([''], axis=1)
    return df

def crawler_twse(date: str) -> pd.DataFrame:
    """
    https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date=20241108&type=ALL&response=json&_=1731257834997
    """
    url = (
        "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?"
        "date={date}&type=ALL&response=json"
    )
    url = url.format(date=date)
    time.sleep(5)
    res = requests.get(url, headers=twse_header())
    if res.json()['stat'] == '很抱歉，沒有符合條件的資料!':
        return pd.DataFrame()
    try:
        resj = res.json()
        if 'tables' in resj:
            df = pd.DataFrame(resj['tables'][8]['data'], columns=resj['tables'][8]['fields'])
            colname = df.columns
        else:
            return pd.DataFrame()
    except BaseException:
        return pd.DataFrame()
    
    if len(df) == 0:
        return pd.DataFrame()
    df = colname_zh2en(df.copy(), colname)
    df['date'] = date
    return df


def main(start_date, end_date):
    date_list = gen_date_list(start_date, end_date)
    for date in date_list:
        logger.info(date)
        df = crawler_twse(date)
        if len(df) > 0:
            # df = clean_data(df.copy())
            # df = check_schema(df.copy()) 
            df.to_csv(f'data/{date}.csv', index=False)
    pass


if __name__ == '__main__':
    start_date, end_date = sys.argv[1:]
    main(start_date, end_date)
    
    
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
        'HTTP/1.1': '200',
        'Server': 'nginx',
        'Date': 'Sun, 10 Nov 2024 16:57:56 GMT',
        'Content-Type': 'application/json;charset=UTF-8',
        'Transfer-Encoding': 'chunked',
        'Connection': 'keep-alive',
        'X-Application-Context': 'application:production',
        'vary': 'accept-encoding',
        'Content-Encoding': 'gzip',
        'Content-Security-Policy': "frame-ancestors 'self' *.twse.com.tw *.tdcc.com.tw http://digitalprocesssyst-epassbook.cdn.hinet.net digitalprocesssys-epassbook.cdn.hinet.net;",
        'X-Content-Type-Options': 'nosniff',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'camera=(),microphone=(),geolocation=(),sync-xhr=*,gyroscope=()',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'Access-Control-Allow-Origin': '*',
    }

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
    a = res.json()
    pass


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
    
    
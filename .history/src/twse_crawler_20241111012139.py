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

def crawler_twse(date: str) -> pd.DataFrame:
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
    
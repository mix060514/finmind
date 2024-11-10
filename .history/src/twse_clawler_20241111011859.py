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

def main(start_date, end_date):
    date_list = gen_date_list(start_date, end_date)
    for date in date_list:
        logger.info(date)
    pass


if __name__ == '__main__':
    start_date, end_date = sys.argv[1:]
    main(start_date, end_date)
    
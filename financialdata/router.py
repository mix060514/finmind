import time
import typing


from loguru import logger
from sqlalchemy import text


from financialdata import clients


def check_alive(connect):
    connect.execute(text("select 1 + 1"))
    
def reconnect(connect_func):
    try:
        connect = connect_func()
    except Exception as e:
        logger.info(
            f"{connect_func.__name__} reconnect error {e}"
        )
    return connect

def check_connect_alive(connect, connect_func):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(f"{connect_func.__name__} connect, error: {e}")
            time.sleep(1)
            connect = reconnect(connect_func)
            return check_connect_alive(connect, connect_func)
    else:
        connect = reconnect(connect_func)
        return check_connect_alive(connect, connect_func)
    

class Router:
    def __init__(self) -> None:
        self._mysql_financialdata_conn = (
            clients.get_mysql_financialdata_conn()
        )

    def check_mysql_financialdata_conn_alive(self):
        self._mysql_financialdata_conn = check_connect_alive(
            self._mysql_financialdata_conn
            , clients.get_mysql_financialdata_conn
        )
        return self._mysql_financialdata_conn

    @property
    def mysql_financialdata_conn(self):
        return self.check_mysql_financialdata_conn_alive()

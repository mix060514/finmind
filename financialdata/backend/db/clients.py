from sqlalchemy import create_engine, text, engine
from financialdata.config import (
    MYSQL_DATA_HOST,
    MYSQL_DATA_USER,
    MYSQL_DATA_PASSWORD,
    MYSQL_DATA_DATABASE,
    MYSQL_DATA_PORT,
)


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{MYSQL_DATA_USER}:{MYSQL_DATA_PASSWORD}"
        f"@{MYSQL_DATA_HOST}:{MYSQL_DATA_PORT}/{MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect


if __name__ == "__main__":
    connect = get_mysql_financialdata_conn()
    print(connect)
    result = connect.execute(text("select 1+1"))
    print(result.fetchone())

import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine


def get_mysql_financialdata_conn():
    address = "mysql+pymysql://root:test@localhost:3306/financialdata"
    engine = create_engine(address)
    connect = engine.connect()
    return connect


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price(
    stock_id,
    start_date,
    end_date
):
    sql= f"""
    select * from TaiwanStockPrice
    where stock_id = '{stock_id}'
      and date between '{start_date}' and '{end_date}';
    """
    mysql_conn = get_mysql_financialdata_conn()
    data_df = pd.read_sql(sql=sql, con=mysql_conn)
    data_dict = data_df.to_dict('records')
    return {"data": data_dict}

import importlib 
import typing

from financialdata.backend import db
from financialdata.tasks.worker import app

@app.task
def crawler(dataset: str, parameter: dict[str,str]):
    df = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "crawler"
    )(parameter=parameter)
    db_dataset = dict(
        taiwan_stock_price = "TaiwanStockPrice",
    )
    db.upload_data(
        df, db_dataset.get(dataset), db.router.mysql_financialdata_conn
    )



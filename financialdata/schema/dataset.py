from pydantic import BaseModel
import importlib

import pandas as pd


class TaiwanStockPrice(BaseModel):
    stock_id: str
    trade_volume: int
    transactions: int
    trade_value: int
    open: float
    max: float
    min: float
    close: float
    change: float
    date: str


def check_schema(df: pd.DataFrame, dataset: str):
    df_dict= df.to_dict('records')
    schema = getattr(
        importlib.import_module(('financialdata.schema.dataset')),
        dataset
    )
    df_schema = [schema(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df

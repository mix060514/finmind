import typing

import pandas as pd
import pymysql
from loguru import logger
from sqlalchemy import engine, text


def update2mysql_by_pandas(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    logger.info("update2mysql_by_pandas")
    if len(df) > 0:
        try:
            df.to_sql(
                name=table,
                con=mysql_conn,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
            mysql_conn.commit()
        except Exception as e:
            logger.info(e)
            mysql_conn.rollback()
            pass


def build_update_sql(colnames: list[str], value: list[str]) -> str:
    update_sql = ",".join(
        [
            ' `{}` = "{}" '.format(colnames[i], str(value[i]))
            for i in range(len(colnames))
            if str(value[i])
        ]
    )
    return update_sql


def build_df_update_sql(table: str, df: pd.DataFrame) -> list[str]:
    logger.info("build_df_udpate_sql")
    df_columns = df.columns.tolist()
    sql_list = []
    for i in range(len(df)):
        temp = list(df.iloc[i])
        value = [pymysql.converters.escape_string(str(v)) for v in temp]
        sub_df_columns = [df_columns[j] for j in range(len(df_columns))]
        update_sql = build_update_sql(
            colnames=sub_df_columns,
            value=value,
        )
        sql = """INSERT `{}`({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}""".format(
            table,
            "`{}`".format("`,`".join(sub_df_columns)),
            '"{}"'.format('","'.join(value)),
            update_sql,
        )
        sql_list.append(sql)
    return sql_list


def update2mysql_by_sql(
    df: pd.DataFrame, table: str, mysql_conn: engine.base.Connection
):
    sql = build_df_update_sql(table=table, df=df)
    commit(sql=sql, mysql_conn=mysql_conn)


def commit(sql: str | list[str], mysql_conn: engine.base.Connection = None):
    logger.info("commit")
    try:
        trans = mysql_conn.begin()
        if isinstance(sql, list):
            for s in sql:
                try:
                    # mysql_conn.execution_options(autocommit=False).execute(s)
                    mysql_conn.execution_options(autocommit=False).execute(text(s))
                except Exception as e:
                    logger.info(e)
                    logger.info(s)
                    break
        elif isinstance(sql, str):
            # mysql_conn.execution_options(autocommit=False).execute(sql)
            mysql_conn.execution_options(autocommit=False).execute(text(sql))
            # maybe it need text(sql)
        trans.commit()
    except Exception as e:
        logger.info(e)
        trans.rollback()


def upload_data(df: pd.DataFrame, table: str, mysql_conn: engine.base.Connection):
    if len(df) > 0:
        if update2mysql_by_pandas(df=df, table=table, mysql_conn=mysql_conn):
            pass
        else:
            update2mysql_by_sql(df=df, table=table, mysql_conn=mysql_conn)

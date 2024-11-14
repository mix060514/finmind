from sqlalchemy import create_engine, text

def get_mysql_financialdata_conn():
    address = "mysql+pymysql://root:test@localhost:3306/financialdata"
    engine = create_engine(address)
    connect = engine.connect()
    return connect

if __name__ == '__main__':
    connect = get_mysql_financialdata_conn()
    print(connect)
    print(connect.execute(text('select 1+1')))


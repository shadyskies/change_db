import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from dotenv import load_dotenv
import os


def mysql_connect(table):
    load_dotenv()
    db_connection_url = f"mysql+mysqldb://django_projects:{os.getenv('django_pwd')}@localhost/{table}"
    db_connection = create_engine(db_connection_url)
    return db_connection


# exports mysql db to csv file in same dir
def mysql_dump(db_connection, table):
    df = pd.read_sql(f"SELECT * FROM {table}", con=db_connection)
    # print cols
    print(df.columns.ravel)
    df.to_csv('frommysql.csv', index=False)


def mysql_load(db_connection, file, name):
    df = pd.read_csv(file)
    if "id" not in df.columns:
        df.to_sql(name, con=db_connection, index=True, if_exists='replace')
    else:
        df.to_sql(name, con=db_connection, index=True, index_label="id", if_exists='replace')


## USAGE
# conn = connect_mysql()
# mysql_dump(db_connection=conn)
# mysql_load(db_connection=conn, file="frompostgres.csv", name="temp1")


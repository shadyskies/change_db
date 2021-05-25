# for outputting to csv -->
# for server side: COPY (SELECT * FROM foo) TO <location> WITH CSV DELIMITER ',' HEADER;
# psycopg2 need to be installed for sql alchemy to work
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import pandas as pd


def pg_connect(db):
    load_dotenv()
    db_connection_url = f"postgresql+psycopg2://postgres:{os.getenv('pg_pwd')}@127.0.0.1/{db}"
    db_connection = create_engine(db_connection_url)
    return db_connection


# dumps to csv in same dir
def pg_dump(db_connection, table):
    df = pd.read_sql(f"SELECT * FROM {table};", con=db_connection)
    # print(df.columns.ravel)
    df.to_csv('frompostgres.csv', index=False)


# load csv to pg using pandas
def pg_load(db_connection, file, name):
    df = pd.read_csv(file)
    if "id" not in df.columns:
        df.to_sql(name, con=db_connection, index=True, index_label='id', if_exists='replace')
    else:
        df.to_sql(name, con=db_connection, index=True, if_exists='replace')


# conn = connect_pg()
# pg_load(conn, "frommysql.csv")
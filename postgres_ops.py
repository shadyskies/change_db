# for outputting to csv -->
# for server side: COPY (SELECT * FROM foo) TO <location> WITH CSV DELIMITER ',' HEADER;
# psycopg2 need to be installed for sql alchemy to work
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import pandas as pd



def connect_pg():
    # load_dotenv()

    db_connection_url = f"postgresql+psycopg2://postgres:postgres_pwd@127.0.0.1/practice"
    db_connection = create_engine(db_connection_url)
    return db_connection


# dumps to csv in same dir
def pg_dump(db_connection):
    df = pd.read_sql("SELECT * FROM emp;", con=db_connection)
    print(df.columns.ravel)
    df.to_csv('frompostgres.csv', index=False)


# load csv to pg
def pg_load(db_connection, file):
    # db_connection = db_connection.raw_connection()
    cur = db_connection.connect()
    df = pd.read_csv(file)
    heads = list(df.head(1))
    vals = df.iloc[1:2, :].values.tolist()
    vals = vals[0]

    print(heads)
    print(vals)
    # print(vals[0])

    # formulate table creation string
    dic = {"str": "VARCHAR[50]", "float": "FLOAT", "int": "INT"}
    tmp = ""
    for i in range(len(vals)):
        tmp1 = vals[i].__class__.__name__
        print(tmp1)
        if i!=len(vals)-1:
            if tmp1 in dic:
                tmp += heads[i] + " " + dic[tmp1] + ", "
        else:
            tmp += heads[i] + " " + dic[tmp1]
    print(tmp)
    create_table = f"CREATE TABLE IF NOT EXISTS temp({tmp});"
    cur.execute(create_table)
    cur.commit()
    cur.close()


conn = connect_pg()
pg_load(conn, "frommysql.csv")
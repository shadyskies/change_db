import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from dotenv import load_dotenv
import os
from sqlalchemy import inspect
import shutil

def mysql_connect(database):
    load_dotenv()
    db_connection_url = f"mysql+mysqldb://django_projects:{os.getenv('django_pwd')}@localhost/{database}"
    db_connection = create_engine(db_connection_url)
    return db_connection


# exports mysql db to csv file in same dir
def mysql_dump(db_connection, table):
    if table != 'all':
        df = pd.read_sql(f"SELECT * FROM {table}", con=db_connection)
        # print(df.columns.ravel)
        df.to_csv('frommysql.csv', index=False)
    else:
        inspector = inspect(db_connection)
        try:
            shutil.rmtree('mysql_dump_all')
        except Exception as e:
            pass
        if not os.path.exists("mysql_dump_all"):
            os.mkdir("mysql_dump_all")
        for table in db_connection.table_names():
            print(f"Dumping table: {table}")
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(f"{query}", con=db_connection)
            df.to_csv(f'mysql_dump_all/{table}.csv', index=False)

# load into mysql db
def mysql_load(db_connection, file, name):
    if file != "all":
        df = pd.read_csv(file)
        if "id" not in df.columns:
            df.to_sql(name, con=db_connection, index=True, if_exists='replace')
        else:
            df.to_sql(name, con=db_connection, index=True, index_label="id", if_exists='replace')
    else:
        files = os.listdir("pg_dump_all")
        for file in files:
            df = pd.read_csv(f"pg_dump_all/{file}")
            file = file.split(".")[0]
            print(f'loading file {file}')
            try:
                if "id" not in df.columns:
                    df.to_sql(file, con=db_connection, index=True, if_exists='replace')
                else:
                    df.to_sql(file, con=db_connection, index=False, index_label="id", if_exists='replace')
            except Exception as e:
                pass
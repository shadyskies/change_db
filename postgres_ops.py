# for outputting to csv -->
# for server side: COPY (SELECT * FROM foo) TO <location> WITH CSV DELIMITER ',' HEADER;
# psycopg2 need to be installed for sql alchemy to work
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
import pandas as pd
from sqlalchemy import inspect
import shutil

def pg_connect(db):
    load_dotenv()
    db_connection_url = f"postgresql+psycopg2://postgres:{os.getenv('pg_pwd')}@127.0.0.1/{db}"
    db_connection = create_engine(db_connection_url)
    return db_connection


# dumps to csv in same dir
def pg_dump(db_connection, table):
    if table != "all":
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(f"{query}", con=db_connection)
        print(df.columns)
        df.to_csv('frompostgres.csv', index=False)
    else:
        inspector = inspect(db_connection)
        try:
            shutil.rmtree('pg_dump_all')
        except Exception as e:
            pass
        if not os.path.exists("pg_dump_all"):
            os.mkdir("pg_dump_all")
        for table in inspector.get_table_names(schema="public"):
            print(f"Dumping table: {table}")
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(f"{query}", con=db_connection)
            df.to_csv(f'pg_dump_all/{table}.csv', index=False)
# load csv to pg using pandas
def pg_load(db_connection, file, name):
    if file != 'all': 
        df = pd.read_csv(file)
        if "id" not in df.columns:
            df.to_sql(name, con=db_connection, index=True, index_label='id', if_exists='replace')
        else:
            df.to_sql(name, con=db_connection, index=True, if_exists='replace')
    else:
        files = os.listdir("mysql_dump_all")
        for file in files:
            df = pd.read_csv(f"mysql_dump_all/{file}")
            file = file.split(".")[0]
            print(f'loading file {file}')
            try:
                if "id" not in df.columns:
                    df.to_sql(file, con=db_connection, index=True, if_exists='replace')
                else:
                    df.to_sql(file, con=db_connection, index=False, index_label="id", if_exists='replace')
            except Exception as e:
                pass
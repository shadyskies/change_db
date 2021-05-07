import pandas as pd
from sqlalchemy import create_engine
import mysql.connector


def export():
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="django_projects",
    #     password="<password>",
    #     database="emp"
    # )
    db_connection_url = f"mysql://django_projects:<password>@localhost/emp"
    db_connection = create_engine(db_connection_url)

    df = pd.read_sql("SELECT * FROM EMPLOYEE", con=db_connection)
    # print cols
    print(df.columns.ravel)
    return df

df = export()
df.to_csv('frommysql.csv', index=False)


from mysql_ops import mysql_connect, mysql_load, mysql_dump
from postgres_ops import pg_connect, pg_dump, pg_load
import os
import argparse


def create_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", type=str, required=True, help="pg/mysql")
    ap.add_argument("-d", "--database", type=str, required=True, help="db name")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    args = create_args()
    if args['type'] == "pg":
        print("[INFO] connecting to postgres")
        conn = pg_connect(args['database'])
        val = int(input("0:Load\n1:Dump: "))
        if val:
            table = input("table name: ")
            print(f"[INFO] Dumping SQL table: {table}")
            pg_dump(conn, args['table'])
        else:
            file = input("Enter csv file path: ")
            name = input("Enter name of table: ")
            pg_load(conn, file, name)
    else:
        print("[INFO] Connecting to MySQL")
        conn = mysql_connect(args["database"])
        val = int(input("0:Export\n1:Load"))
        if val:
            file = input("Enter csv file path: ")
            name = input("Enter name of : ")
            print("[INFO] Loading to MySQL")
            mysql_load(conn, file, name)
        else:
            table = input("table name: ")
            print(f"[INFO] Dumping SQL table: {table}")
            mysql_dump(conn, table)
            
    print("Operation executed successfully")
    
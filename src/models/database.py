# import mysql.connector
import pymysql
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('.env')

load_dotenv(dotenv_path = dotenv_path)
host=os.getenv('DB_HOST')
user=os.getenv('DB_USERNAME')
password=os.getenv('DB_PASSWORD')
database=os.getenv('DB_NAME')
port=int(os.getenv('DB_PORT'))

class DBConnection:


    def __init__(self):
        self.mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,

        )
        self.cursor = self.mydb.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mydb.commit()
        self.mydb.close()

    # def adduser(self, query, *details):
    #     response = None
    #     with DBConnection() as cursor:
    #         try:
    #             cursor.execute(query, details)
    #         except mysql.connector.Error as error:
    #             print(error)
    #             raise error
    #             # return False
    #         return True
    def adduser(self, query, *details):
        response = None
        with DBConnection() as cursor:
            try:
                cursor.execute(query, details)
            except pymysql.Error as error:
                print(error)
                raise error
                # return False
            return True

    def get_item(self, query, *data):
        response = None
        with DBConnection() as cursor:
            try:
                cursor.execute(query, *data)
                response = cursor.fetchone()
            except pymysql.Error as error:
                print(error)
                raise error
            return response

    def get_items(self, query, data):
        response = None
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
                response = cursor.fetchall()
            except pymysql.Error as error:
                print(error)
                raise error
            return response

    def update_items(self, query, *data):
        items = None
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
            except pymysql.Error as error:
                print(error)
                raise error
            return True

    def check_item(self, query, *data):
        items = None
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
                response = cursor.fetchone()[0]
            except pymysql.Error as error:
                print(error)
                raise error
            return response > 0

    def remove_item(self, query, *data):
        with DBConnection() as cursor:
            try:
                cursor.execute(query, data)
            except pymysql.Error as error:
                print(error)
                raise error
            return True

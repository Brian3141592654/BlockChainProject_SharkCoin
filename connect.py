import pymysql
from dbutils.pooled_db import PooledDB

def connectPool():
    pool = PooledDB(pymysql,5,
                    host='112.104.189.126',
                    user='admin',
                    passwd='12345678',
                    db='sharkcoin',
                    port=3306,
                    setsession=['SET AUTOCOMMIT = 1']
                )
    return pool

def connect():
    mysqldb = pymysql.connect(
            host="112.104.189.126",
            user="admin",
            passwd="12345678",
            database="sharkcoin")
    return mysqldb

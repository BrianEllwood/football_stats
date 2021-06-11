import os
from flask import Flask
import mysql.connector

class DBManager:
    def __init__(cnx, database='footstat2', host='localhost', user="root", password_file=None):
        #pf = open(password_file, 'r')
        cnx.connection = mysql.connector.connect(
            user=user, 
            password='ten2ten-zz',
            host=host, # name of the mysql service as set in the docker-compose file
            database=database,
            port='6603',
            auth_plugin='mysql_native_password'
        )
        #pf.close()
        cnx.cursor = cnx.connection.cursor(buffered=True)
    
    def query_matchday(cnx):
        print("test2 -----------------------------------")
        cnx.cursor.execute('select * from matchday;')
        print("test3 -----------------------------------")
        rec = []
        for c in cnx.cursor:
            rec.append(c)
        return rec


#server = Flask(__name__)
conn = None

#@server.route('/')
def listBlog():
    print("test1 -----------------------------------")
    global conn
    if not conn:
        conn = DBManager()
        #conn.populate_db()
    rec = conn.query_matchday()

    response = ''
    for c in rec:
        c=str(c)
        response = response  + '<div>   <font size="+2">' +c + '</font> </div>'
    return response


if __name__ == '__main__':
    fred=listBlog()
    print("fred---",fred)



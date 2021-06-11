import os
from flask import Flask
import mysql.connector

class DBManager:
    def __init__(cnx, database='footstat2', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        cnx.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker-compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        cnx.cursor = cnx.connection.cursor()
    
    def query_matchday(cnx):
        cnx.cursor.execute('select * from matchday;')
        rec = []
        for c in cnx.cursor:
            rec.append(c)
        return rec


server = Flask(__name__)
conn = None

@server.route('/')
def listBlog():
    
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
    rec = conn.query_matchday()

    response = ''
    for c in rec:
        c=str(c)
        c=c.replace("(",'')
        c=c.replace(')','')
        c=c.replace("'",'')
        c=c.replace("datetime.date",'')
        response = response  + '<div>   <font size="-1">' + c + '</font> </div>'
    return response


if __name__ == '__main__':
    server.run()

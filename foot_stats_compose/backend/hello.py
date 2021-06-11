import os
from flask import Flask
import mysql.connector

class DBManager:
    def __init__(self, database='footstat2', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker-compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Bog postzz #%d'% i) for i in range (1,6)])
        self.connection.commit()
    
    def query_matchday(self):
        self.cursor.execute('select * from matchday;')
        rec = []
        for c in self.cursor:
            rec.append(c)
        return rec


server = Flask(__name__)
conn = None

@server.route('/')
def listBlog():
    print("test1 -----------------------------------")
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        #conn.populate_db()
    rec = conn.query_matchday()

    response = ''
    for c in rec:
        c=str(c)
        response = response  + '<div>   ' + c + '</div>'
    return response


if __name__ == '__main__':
    server.run()

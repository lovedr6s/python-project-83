import psycopg2
from utils import DATABASE_URL
import datetime

conn = psycopg2.connect(DATABASE_URL)

def get_url_by_id(id):
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls WHERE id = %s", (id, ))
        data = curs.fetchone()
        return data[1]

def get_id_by_name(name):
    with conn.cursor() as curs:
        curs.execute('SELECT id FROM urls WHERE name = %s', (name,))
        return curs.fetchone()

def get_all_urls():
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls ORDER BY id")
        return curs.fetchall()
    
def insert_data_into_urls(data):
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (data, datetime.datetime.now()))
        id = curs.fetchone()[0]
        conn.commit()
        return id
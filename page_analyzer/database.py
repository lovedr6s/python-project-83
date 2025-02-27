import psycopg2
from page_analyzer.utils import DATABASE_URL
import datetime

conn = psycopg2.connect(DATABASE_URL)

def get_url_by_id(id):
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls WHERE id = %s", (id, ))
        data = curs.fetchone()
        return data

def get_id_by_name(name):
    with conn.cursor() as curs:
        curs.execute('SELECT id FROM urls WHERE name = %s', (name,))
        return curs.fetchone()

def get_all_urls():
    with conn.cursor() as curs:
        curs.execute("SELECT DISTINCT ON (urls.id) urls.id, urls.name, url_checks.created_at FROM urls INNER JOIN url_checks ON url_checks.url_id = urls.id WHERE url_checks.created_at = ( SELECT created_at FROM url_checks ORDER BY created_at DESC LIMIT 1 ) ORDER BY id")
        return curs.fetchall()
    
def insert_data_into_urls(data):
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (data, datetime.date.today()))
        id = curs.fetchone()[0]
        conn.commit()
        return id


def insert_data_into_url_checks(data):
    with conn.cursor() as curs:
        curs.execute('INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)', (data, datetime.date.today()))
        conn.commit()


def get_data_from_url_checks_by_id(data):
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM url_checks WHERE url_id = %s', (data, ))
        return curs.fetchall()
import psycopg2
from page_analyzer.utils import DATABASE_URL
from page_analyzer.site_request_data import get_site_data, get_page_data
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
        curs.execute("SELECT DISTINCT ON (urls.id) urls.id, urls.name, url_checks.created_at, url_checks.status_code FROM urls LEFT JOIN url_checks ON url_checks.url_id = urls.id AND url_checks.id = ( SELECT MAX(id) FROM url_checks WHERE url_id = urls.id) ORDER BY urls.id")
        return curs.fetchall()
    
def insert_data_into_urls(data):
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (data, datetime.date.today()))
        id = curs.fetchone()[0]
        conn.commit()
        return id


def insert_data_into_url_checks(data, site):
    with conn.cursor() as curs:
        if site[0] == 'error':
            curs.execute('INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s)', (data, site[1], datetime.date.today()))
        else:
            curs.execute('INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)', (data, get_site_data(site)[1].status_code, get_page_data(site)['h1'], get_page_data(site)['title'], get_page_data(site)['description'],  datetime.date.today()))
        conn.commit()


def get_data_from_url_checks_by_id(data):
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM url_checks WHERE url_id = %s', (data, ))
        return curs.fetchall()

def get_name_from_urls_by_id(id):
    with conn.cursor() as curs:
        curs.execute("SELECT name FROM urls WHERE id = %s", (id, ))
        return curs.fetchone()[0]
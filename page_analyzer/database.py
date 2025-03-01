import psycopg2
from page_analyzer.utils import DATABASE_URL
from page_analyzer.site_request_data import get_site_data, get_page_data
import datetime


def with_connection(func):
    def wrapper(*args, **kwargs):
        with psycopg2.connect(DATABASE_URL) as conn, conn.cursor() as cursor:
            return func(cursor, *args, **kwargs)
    return wrapper


@with_connection
def get_url_by_id(cursor, id):
    cursor.execute("SELECT * FROM urls WHERE id = %s", (id, ))
    return cursor.fetchone()


@with_connection
def get_id_by_name(cursor, name):
    cursor.execute('SELECT id FROM urls WHERE name = %s', (name,))
    return cursor.fetchone()


@with_connection
def get_all_urls(cursor):
    query = """
    SELECT DISTINCT ON (urls.id) urls.id, urls.name,
    url_checks.created_at, url_checks.status_code
    FROM urls
    LEFT JOIN url_checks
    ON url_checks.url_id = urls.id
    AND url_checks.id = ( SELECT MAX(id)
    FROM url_checks WHERE url_id = urls.id)
    ORDER BY urls.id DESC
    """

    cursor.execute(query)
    return cursor.fetchall()


@with_connection
def insert_data_into_urls(cursor, name):
    query = '''
    INSERT INTO urls (name, created_at)
    VALUES (%s, %s) RETURNING id
    '''
    cursor.execute(query, (name, datetime.date.today()))
    cursor.connection.commit()
    return cursor.fetchone()[0]


@with_connection
def insert_data_into_url_checks(cursor, url_id, site):
    site_data = get_site_data(site)
    page_data = get_page_data(site)
    query = """
    INSERT INTO url_checks
    (url_id, status_code, h1, title, description, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (url_id,
              site_data.status_code,
              page_data['h1'],
              page_data['title'], 
              page_data['description'],
              datetime.date.today())

    cursor.execute(query, values)
    cursor.connection.commit()
    return True


@with_connection
def get_data_from_url_checks_by_id(cursor, url_id):
    cursor.execute('SELECT * FROM url_checks WHERE url_id = %s', (url_id, ))
    return cursor.fetchall()


@with_connection
def get_name_from_urls_by_id(cursor, url_id):
    cursor.execute("SELECT name FROM urls WHERE id = %s", (url_id, ))
    return cursor.fetchone()[0]

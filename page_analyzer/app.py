from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from urllib.parse import urlparse
import datetime
import validators
import psycopg2
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/urls')
def add_url():
    url = request.form.get('url')

    if not url or not validators.url(url) or len(url) > 255:
        flash("Некорректный url")
        return redirect(url_for('index'))
    
    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    with conn.cursor() as curs:

        curs.execute('SELECT id FROM urls WHERE name = %s', (normalized_url,))
        existing_url = curs.fetchone()
        if existing_url:
            flash("Такой url уже существует")
            return redirect(url_for('index', url_id=existing_url[0]))
        
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (normalized_url, datetime.datetime.now()))
        url_id = curs.fetchone()[0]
        conn.commit()
        flash("URL добавлен")
        return redirect(url_for("show_url", id=url_id))

@app.route("/urls")
def show_urls():
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls ORDER BY id")
        urls = curs.fetchall()
        return render_template('urls.html', urls=urls)

@app.get('/urls/<id>')
def show_url(id):
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls WHERE id = %s", (id, ))
        url_data = curs.fetchone()
        return render_template('url.html', url=url_data)

        
   

if __name__ == "__main__":
    app.run(debug=True)
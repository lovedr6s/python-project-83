from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from database import *
from urllib.parse import urlparse
import validators
import os

load_dotenv()

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

    existing_url = get_id_by_name(normalized_url)
    if existing_url:
        flash("Такой url уже существует")
        return redirect(url_for('show_url', id=existing_url[0]))
    
    url_id = insert_data_into_urls(normalized_url)
    conn.commit()
    flash("URL добавлен")
    return redirect(url_for("show_url", id=url_id))

@app.route("/urls")
def show_urls():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)

@app.get('/urls/<int:id>')
def show_url(id):
    url_data = get_url_by_id(id)
    return render_template('url_detaly.html', url=url_data[1])


@app.post('/urls/<int:id>/checks')
def check_url(id):
    with conn.cursor() as curs:
        curs.execute("INSERT INTO url_checks (created_at) VALUES (%s)", (datetime.datetime.now()))

    return redirect(url_for('show_url', id=id))
    
   

if __name__ == "__main__":
    app.run(debug=True)
from flask import (
    Flask, render_template, redirect, url_for, request, flash
)
from page_analyzer.database import (
    fetch_url_by_id, fetch_id_by_name, fetch_all_urls,
    add_urls_to_db, add_url_check,
    fetch_url_checks_by_id, fetch_url_name_by_id
)
from page_analyzer.utils import SECRET_KEY
from page_analyzer.site_request_data import (
    extract_page_info, fetch_site_response
)
from urllib.parse import urlparse
import validators


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.get('/')
def index():
    return render_template('index.html')


def validate_url(url):
    if not url or not validators.url(url) or len(url) > 255:
        return False
    return True


@app.post('/urls')
def handle_add_url():
    url = request.form.get('url')

    if not validate_url(url):
        flash("Некорректный URL")
        return render_template('index.html'), 422

    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    is_url_exists = fetch_id_by_name(normalized_url)

    if is_url_exists:
        flash("Страница уже существует")
        return redirect(url_for('show_url_details', id=is_url_exists[0]))

    url_id = add_urls_to_db(normalized_url)
    flash("Страница успешно добавлена")
    return redirect(url_for("show_url_details", id=url_id))


@app.route("/urls")
def list_urls():
    return render_template('urls.html', urls=fetch_all_urls())


@app.get('/urls/<int:id>')
def show_url_details(id):
    url_name = fetch_url_by_id(id)

    if not url_name:
        flash('URL не найден')
        return redirect(url_for('index'))

    url_check = fetch_url_checks_by_id(id)
    if not url_check:
        return render_template('url_detaly.html', url=url_name, id=id)
    return render_template('url_detaly.html',
                           url_check_data=url_check,
                           url=url_name, id=id)


@app.get('/urls/<int:id>/details')
def redirect_to_url_details(id):
    return redirect(url_for('show_url_details', id=id))


@app.post('/urls/<int:id>/checks')
def perfom_check_url(id):
    url = fetch_url_name_by_id(id)
    site_data = fetch_site_response(url)
    page_data = extract_page_info(url)
    if not url:
        flash('URL не найден')
        return redirect(url_for('redirect_to_url_details', id=id))

    if site_data == 'error' or page_data == 'error':
        flash('Произошла ошибка при проверке')
        return redirect(url_for('redirect_to_url_details', id=id))
    add_url_check(id, url)
    flash('Страница успешно проверена')
    return redirect(url_for('redirect_to_url_details', id=id))

from flask import (
    Flask, render_template, redirect, url_for, request, flash
)
from page_analyzer.database import (
    get_url_by_id, get_id_by_name, get_all_urls,
    insert_data_into_urls, insert_data_into_url_checks,
    get_data_from_url_checks_by_id, get_name_from_urls_by_id
)
from page_analyzer.utils import SECRET_KEY
from page_analyzer.site_request_data import get_page_data, get_site_data
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
def add_url():
    url = request.form.get('url')

    if not validate_url(url):
        flash("Некорректный URL")
        return render_template('index.html'), 422

    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    existing_url = get_id_by_name(normalized_url)

    if existing_url:
        flash("Страница уже существует")
        return redirect(url_for('show_url', id=existing_url[0]))

    url_id = insert_data_into_urls(normalized_url)
    flash("Страница успешно добавлена")
    return redirect(url_for("show_url", id=url_id))


@app.route("/urls")
def show_urls():
    return render_template('urls.html', urls=get_all_urls())


@app.get('/urls/<int:id>')
def url_detail(id):
    url_name = get_url_by_id(id)

    if not url_name:
        flash('URL не найден')
        return redirect(url_for('index'))

    url_check = get_data_from_url_checks_by_id(id)
    if not url_check:
        return render_template('url_detaly.html', url=url_name, id=id)
    return render_template('url_detaly.html',
                           url_check_data=url_check,
                           url=url_name, id=id)


@app.get('/urls/<int:id>/details')
def show_url(id):
    return redirect(url_for('url_detail', id=id))


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = get_name_from_urls_by_id(id)
    site_data = get_site_data(url)
    page_data = get_page_data(url)
    if not url:
        flash('URL не найден')
        return redirect(url_for('show_url', id=id))

    if site_data == 'error' or page_data == 'error':
        flash('Произошла ошибка при проверке')
        return redirect(url_for('show_url', id=id))
    insert_data_into_url_checks(id, url)
    flash('Страница успешно проверена')
    return redirect(url_for('show_url', id=id))


if __name__ == "__main__":
    app.run(debug=True)

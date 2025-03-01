from flask import (
    Flask, render_template, redirect, url_for, request, flash
)
from page_analyzer.database import (
    get_url_by_id, get_id_by_name, get_all_urls,
    insert_data_into_urls, insert_data_into_url_checks,
    get_data_from_url_checks_by_id, get_name_from_urls_by_id
)
from page_analyzer.utils import SECRET_KEY
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
        return redirect(url_for('index'))

    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    existing_url = get_id_by_name(normalized_url)

    if existing_url:
        flash("Такой url уже существует")
        return redirect(url_for('show_url', id=existing_url[0]))

    url_id = insert_data_into_urls(normalized_url)
    flash("URL добавлен")
    return redirect(url_for("show_url", id=url_id))


@app.route("/urls")
def show_urls():
    return render_template('urls.html', urls=get_all_urls())


@app.get('/urls/<int:id>')
def url_detail(id):
    url_data = get_url_by_id(id)

    if not url_data:
        flash('URL не найден')
        return redirect(url_for('index'))

    url_check = get_data_from_url_checks_by_id(url_data[0])
    return render_template('url_detaly.html',
                           url_check_data=url_check,
                           url=url_data, id=url_data[0])


@app.get('/urls/<int:id>/details')
def show_url(id):
    return redirect(url_for('url_detail', id=id))


@app.post('/urls/<int:id>/checks')
def check_url(id):
    insert_data_into_url_checks(id, get_name_from_urls_by_id(id))
    flash('Страница успешно проверенна')
    return redirect(url_for('show_url', id=id))


if __name__ == "__main__":
    app.run(debug=True)

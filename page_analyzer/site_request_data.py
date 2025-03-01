import requests
from bs4 import BeautifulSoup


def get_site_data(site):
    try:
        response = requests.get(site)
        if response.status_code != 200:
            return ('error', response)
        return ('succses', response)
    except requests.exceptions.RequestException:
        return ('error', type('FakeResponse', (object,),
                              {'status_code': 400})())


def get_page_data(site):
    try:
        response = requests.get(site)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="html.parser")
        title = soup.title.text.strip() if soup.title else None

        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else None

        h1 = soup.find('h1').text.strip() if soup.find('h1') else None
        return {'title': title,
                'h1': h1,
                'description': description}
    except requests.exceptions.RequestException:
        return 'error'

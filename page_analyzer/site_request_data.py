import requests
from bs4 import BeautifulSoup

def get_site_data(site):
    try:
        site = requests.get(site)
        if site.status_code != 200:
            return ('error', site)
        return ('succses', site)
    except:
        return ('error', type('FakeResponse', (object,), {'status_code': 400})())

def get_page_data(site):
    try:
        site = requests.get(site)
        soup = BeautifulSoup(site.text)
        title = soup.title.text.strip() if soup.title else None
        description = soup.find('meta', attrs={'name': 'description'})['content']
        h1 = soup.find('h1').text.strip() if soup.find('h1') else None
        return {'title': title, 'h1': h1, 'description': description}
    except:
        return {'title': 'None', 'h1': 'None', 'description': 'None'}
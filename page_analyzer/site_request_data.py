import requests
from bs4 import BeautifulSoup

def check_site_availability(site):
    try:
        response = requests.get(site)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        return False

def get_site_data(site):
    response = check_site_availability(site)
    return response


def get_page_data(site):
    if not check_site_availability(site):
        return 'error'
    soup = BeautifulSoup(check_site_availability(site).text, features="html.parser")
    title = soup.title.text.strip() if soup.title else ''

    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'] if meta_description else ''
    h1 = soup.find('h1').text.strip() if soup.find('h1') else ''
    return {'title': title,
            'h1': h1,
            'description': description}

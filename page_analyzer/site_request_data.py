import requests
from bs4 import BeautifulSoup


def is_site_available(site):
    try:
        response = requests.get(site)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException:
        return False


def fetch_site_response(site):
    response = is_site_available(site)
    return response


def extract_page_info(site):
    if not is_site_available(site):
        return 'error'
    soup = BeautifulSoup(
        is_site_available(site).text, features="html.parser"
        )

    meta_description = soup.find('meta', attrs={'name': 'description'})

    return {'title': soup.title.text.strip() if soup.title else '',
            'h1': soup.find('h1').text.strip() if soup.find('h1') else '',
            'description': meta_description['content'] if meta_description
            else ''
            }

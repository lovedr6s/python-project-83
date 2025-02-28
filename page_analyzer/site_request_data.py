import requests

def get_site_data(site):
    try:
        site = requests.get(site)
        if site.status_code != 200:
            return ('error', site)
        return ('succses', site)
    except:
        return ('error', type('FakeResponse', (object,), {'status_code': 400})())

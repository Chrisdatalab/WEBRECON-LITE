import requests

def http_get(url):
    r = requests.get(url)
    return r
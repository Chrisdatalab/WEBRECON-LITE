import requests

def http_get(url):
    try:
        r = requests.get(url,timeout=10)
        
    except requests.exceptions.Timeout:
        print("REQUEST TIMEOUT")
        return None
    except requests.exceptions.RequestException:
        print("REQUEST FAILED")
        return None
    return r
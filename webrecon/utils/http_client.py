import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "WEBRECON-LITE/0.2.1"
})

def http_get(url):
    try:
        response = session.get(
                                url,
                                timeout=(5, 10),
                                allow_redirects=True
                            )
        return response             
    except requests.exceptions.Timeout as error:
        print(f"REQUEST TIMEOUT: {url}")
        print(error)

    except requests.exceptions.SSLError as error:
        print(f"SSL ERROR: {url}")
        print(error)

    except requests.exceptions.ConnectionError as error:
        print(f"CONNECTION ERROR: {url}")
        print(error)

    except requests.exceptions.RequestException as error:
        print(f"REQUEST FAILED: {url}")
        print(error)
    return None
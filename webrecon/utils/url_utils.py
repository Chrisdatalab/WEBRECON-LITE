from urllib.parse import urlparse, urldefrag

def normalize_url(url):

    url, _ = urldefrag(url)
    if url.endswith("/") and len(url) > len("https://"):
        return url.rstrip("/")
    else:
        return url
def get_host(url):
  
    return urlparse(url).hostname

def is_url_in_scope(url, target_host):
    try:
        parsed_url = urlparse(url)
        return (
        parsed_url.scheme.lower() in ("http", "https")
        and parsed_url.hostname == target_host
    )
    except ValueError:
        return False

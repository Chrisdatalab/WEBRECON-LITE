from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse

def extract_javascript(html, base_url):
    
    external_scripts=[]
    inline_scripts=[]
    soup=BeautifulSoup(html, "lxml")
    scripts = soup.find_all("script")
    seen_js=set()
   
    for script in scripts:
        src = script.get("src")
        if src:     
            full_link = urljoin(base_url,src)
            scheme = urlparse(full_link).scheme.lower()
            if scheme not in ("http", "https"):
                continue
            if full_link in seen_js:
                continue
            seen_js.add(full_link)
            external_scripts.append(full_link)
        else:
            script_content = script.get_text(strip=True)
            if script_content:
                inline_scripts.append(script_content)
    return {
            "external_scripts": external_scripts,
            "inline_scripts": inline_scripts
        }
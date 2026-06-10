from bs4 import BeautifulSoup
from urllib.parse import urljoin
def extract_links(r,bs_link):
    # Parse the HTML response
    soup=BeautifulSoup(r.text, "lxml")
    # Create a dictionary to store extracted data
    result={}
    # Store extracted links and forms
    web_links=[]
    web_forms=[]

    # Extract status code
    web_status=r.status_code
    # Extract page title safely
    if soup.title and soup.title.text:
        web_title=soup.title.text
    else:
        web_title=None
    # Store response headers
    web_serverHead=r.headers
    # Extract and normalize all links
    for a in soup.find_all("a"):
        href = a.get("href")
        if(href):
            full_link = urljoin(bs_link,href)
            web_links.append(full_link)
    # Remove duplicate links      
    web_links = list(set(web_links))
    # Extract and normalize all forms
    for f in soup.find_all("form"):
        form_arrtres=['action','method']
        form={}
        for value in form_arrtres:
            if(f.get(value)):
                form[value]=f[value]
        if(form):
            web_forms.append(form)
    # Save in a dic
    result['title']=web_title
    result['status']=web_status
    result['header']=web_serverHead
    result['links']=web_links
    result['forms']=web_forms
    
    return result
      
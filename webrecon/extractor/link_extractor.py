from bs4 import BeautifulSoup
from urllib.parse import urljoin
def extract_links(r,base_link):
    # Parse the HTML response
    soup=BeautifulSoup(r.text, "lxml")
    # Create a dictionary to store extracted data
    result={}
    # Store extracted links and forms
    web_links=[]
    seen_links = set()
    web_forms=[]

    # Extract status code
    web_status=r.status_code
    # Extract page title safely
    if soup.title and soup.title.text:
        web_title=soup.title.get_text(strip=True)
    else:
        web_title=None
    # Store response headers
    web_serverHead=dict(r.headers)
    # Extract and normalize all links
    for a in soup.find_all("a"):
        href = a.get("href")
        if(href):
            full_link = urljoin(base_link,href)
            if full_link not in seen_links:
                web_links.append(full_link)
                seen_links.add(full_link)
    # Remove duplicate links      
   # web_links = list(set(web_links))
    # Extract and normalize all forms
    # Form structure:
    # {
    #     "action": str,
    #     "method": str,
    #     "inputs": list
        ''' {
            "name": "username",
            "type": "text",
            "id": "user",
            "placeholder": "Username"
        }'''
    # }
    for f in soup.find_all("form"):
        form = {}

    # Extract form action and normalize it to a full URL
        action = f.get("action")
        if action:
            form["action"] = urljoin(base_link, action)
        else:
            form["action"] = None

        # Extract form method, default is GET if not specified
        method = f.get("method")
        if method:
            form["method"] = method.lower()
        else:
            form["method"] = "get"

        # Extract input fields
        inputs = []

        for input_tag in f.find_all("input"):
            input_data = {
                "name": input_tag.get("name"),
                "type": input_tag.get("type"),
                "id": input_tag.get("id"),
                "placeholder": input_tag.get("placeholder")
            }

            inputs.append(input_data)

        form["inputs"] = inputs

        web_forms.append(form)

    # Save in a dic
    result['title']=web_title
    result['status_code']=web_status
    result['headers']=web_serverHead
    result['links']=web_links
    result['forms']=web_forms
    
    return result
      
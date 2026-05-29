from bs4 import BeautifulSoup

def extract_links(r):

    soup=BeautifulSoup(r.text, "lxml")
    resolve={}
    web_status=r.status_code
    web_links=[]
    web_title=soup.title.text
    web_forms=[]
    web_serverHead=r.headers
    print(web_title)
    for a in soup.find_all("a"):
        if(a.get('href')):
            web_links.append(a['href'])
           # print(a['href'])
    web_links = list(set(web_links))
   # print("\n".join(web_links))
    for f in soup.find_all("form"):
        form_arrtres=['action','method']
        form={}
        for value in form_arrtres:
            if(f.get(value)):
                form[value]=f[value]
        if(form):
            web_forms.append(form)
    # Save in a dic
    resolve['title']=web_title
    resolve['status']=web_status
    resolve['header']=web_serverHead
    resolve['links']=web_links
    resolve['forms']=web_forms
    
    return resolve
      
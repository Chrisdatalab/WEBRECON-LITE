
def print_report(result):
    print("WEB RECON REPORT") 
    print("Title:")   
    print(result['title'])
    print("Status:")   
    print(result['status'])   
    print("Links Found:")  
    print(len(result['links']))  
    print("Forms Found:")  
    print(len(result['forms']))
    print("SHOW LINKS(First 10)")
    for link in result['links'][:10]:
        print(link)
    print("SHOW FORMS")
    for form in result['forms']:
        print(form)
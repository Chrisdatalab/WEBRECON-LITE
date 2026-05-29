
def print_report(reslove):
    print("WEB RECON REPORT") 
    print("Title:")   
    print(reslove['title'])
    print("Status:")   
    print(reslove['status'])   
    print("Links Found:")  
    print(len(reslove['links']))  
    print("Forms Found:")  
    print(len(reslove['forms']))
    print("SHOW LINKS(First 10)")
    for link in reslove['links'][:10]:
        print(link)
    print("SHOW FORMS")
    for form in reslove['forms']:
        print(form)
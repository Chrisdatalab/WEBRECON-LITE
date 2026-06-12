import json,os
def save_json_report(result, filepath="reports/report.json"):
    folder = os.path.dirname(filepath)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(f"JSON report saved to: {filepath}")
def print_report(result):
    if result is None:
        print("FAILED")
        return 0
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
'''
    link_analysis = {
    "total_links": 0,
    "internal_links": [],
    "external_links": [],
    "javascript_files": [],
    "document_files": [],
    "possible_api_endpoints": [],
    "login_or_admin_paths": [],
    "parameterized_links": []
}
'''

def link_analysis(links,curr_link):
    # Analyze all links found on curr_link.
    
    print("\n[LINK ANALYZER DEBUG]")
    print("Current page:", curr_link)
    print("Links found:", len(links))

    for link in links:
        print(" -", link)

    return {
        "total_links": len(links)
    }
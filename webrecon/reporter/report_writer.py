import json,os
def save_json_report(result, filepath="reports/report.json"):
    folder = os.path.dirname(filepath)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(f"JSON report saved to: {filepath}")
def print_summary(result):
    # result is the full crawl report.
    # It contains scan-level metadata and a "pages" list.
    # Each item in result["pages"] is one crawled page's extracted data.

    '''
    result structure:

    result = {
        "target": str,          # target URL
        "max_depth": int,       # crawl depth limit
        "max_pages": int,       # max pages limit
        "pages_crawled": int,   # number of pages successfully crawled
        "visited_urls": list,   # crawled URLs in order
        "pages": list           # detailed results for each page
    }

    each page in result["pages"] = {
        "url": str,
        "depth": int,
        "title": str,
        "status_code": int,
        "links": list,
        "forms": list,
        "analysis": dict
    }
    '''
    if result is None:
        print("No result to display.")
        return
    pages = result.get("pages", [])

    total_links = 0
    total_forms = 0

    for page in pages:
        total_links += len(page.get("links", []))
        total_forms += len(page.get("forms", []))
    print("target: ",result.get("target", "N/A"))
    print("max_depth: ",result.get("max_depth", "N/A"))
    print("max_pages: ",result.get("max_pages", "N/A"))
    print("pages_crawled: ",result.get("pages_crawled", 0))
    print("Visited URLs: ",len(result.get("visited_urls", [])))
    print("Total Links Found: ",total_links)
    print("Total Forms Found: ",total_forms)
def print_details(result):
    if result is None:
        print("NO RESULT TO DISPLAY")
        return
    # print_summary(result)
    # print("WEB RECON REPORT")
    # print("=" * 50)

    # New crawler result: multi-page report
    if "pages" in result:
        print(f"Target: {result.get('target', 'N/A')}")
        print(f"Max Depth: {result.get('max_depth', 'N/A')}")
        print(f"Max Pages: {result.get('max_pages', 'N/A')}")
        print(f"Pages Crawled: {result.get('pages_crawled', 0)}")
        print()

        pages = result.get("pages", [])

        if not pages:
            print("No pages crawled.")
            return

        for index, page in enumerate(pages, start=1):
            print(f"[Page {index}]")
            print(f"URL: {page.get('url', 'N/A')}")
            print(f"Depth: {page.get('depth', 'N/A')}")
            print(f"Title: {page.get('title', 'N/A')}")
            print(f"Status Code: {page.get('status_code', 'N/A')}")

            links = page.get("links", [])
            forms = page.get("forms", [])

            print(f"Links Found: {len(links)}")
            print(f"Forms Found: {len(forms)}")

            analysis = page.get("analysis", {})
            link_analysis = analysis.get("links", {})

            if link_analysis:
                print("Link Analysis:")
                for key, value in link_analysis.items():
                    if isinstance(value, list):
                        print(f"  {key}: {len(value)}")
                    else:
                        print(f"  {key}: {value}")

            print("-" * 50)

        return

    # Old single-page result fallback
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Status Code: {result.get('status_code', 'N/A')}")
    print(f"Links Found: {len(result.get('links', []))}")
    print(f"Forms Found: {len(result.get('forms', []))}")
def print_report(result):
    if result is None:
        print("No result to display.")
        return
    print_summary(result)
    print_details(result)
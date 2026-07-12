from collections import deque
from urllib.parse import urlparse, urldefrag
from webrecon.extractor import link_extractor,js_extractor
from webrecon.utils import http_client,url_utils
from webrecon.analyzer import link_analyzer, js_analyzer,header_analyzer
    
def crawler_source_http(source, depth=1, m_pages=20):
    visited = set()
    visited_order = []
    queued = set()
    pages = []

    source = url_utils.normalize_url(source)
    target_host = url_utils.get_host(source)

    q = deque()
    q.append((source, 0))
    queued.add(source)

    while q and len(pages) < m_pages:
        curr_link, current_depth = q.popleft()
        curr_link = url_utils.normalize_url(curr_link)

        if curr_link in visited:
            continue

        if not url_utils.is_url_in_scope(curr_link, target_host):
            continue

        r = http_client.http_get(curr_link)

        if r is None:
            continue
        
        final_url = url_utils.normalize_url(r.url)

        if not url_utils.is_url_in_scope(final_url, target_host):
            print(
                f"SKIPPED OUT-OF-SCOPE REDIRECT: "
                f"{curr_link} -> {final_url}"
            )
            continue
        if final_url in visited and final_url != curr_link:
            visited.add(curr_link)
            continue
        content_type = r.headers.get("Content-Type", "").lower()
        if "text/html" not in content_type:
            print(
                f"SKIPPED NON-HTML CONTENT: "
                f"{final_url} ({content_type or 'unknown'})"
            )
            continue
        visited.add(curr_link)
        visited.add(final_url)
        visited_order.append(final_url)

        result = link_extractor.extract_links(r, final_url)
        headers_result=header_analyzer.analyze_headers(r.headers, final_url)
        javascript_result = js_extractor.extract_javascript(r.text,final_url)
        links = result.get("links", [])

        link_analysis = link_analyzer.link_analysis(links,final_url)
        
        javascript_analysis = js_analyzer.analyze_javascript(javascript_result,final_url)
        result["url"] = final_url
        result["requested_url"] = curr_link
        result["depth"] = current_depth
        result["status_code"] = r.status_code
        result["content_type"] = content_type
        result["redirects"] = [
            redirect.url for redirect in r.history
        ]
        result["analysis"] = {
            "links": link_analysis,
            "javascript": {
                            "extracted": javascript_result,
                            "analysis": javascript_analysis
                        },
            "headers":headers_result
        }
        
        pages.append(result)

        if current_depth < depth:
            for new_link in links:
                new_link = url_utils.normalize_url(new_link)
                if not url_utils.is_url_in_scope(new_link, target_host):
                    continue

                if new_link not in visited and new_link not in queued:
                    q.append((new_link, current_depth + 1))
                    queued.add(new_link)

    final_result = {
        "target": source,
        "max_depth": depth,
        "max_pages": m_pages,
        "pages_crawled": len(pages),
        "visited_urls": visited_order,
        "pages": pages
    }

    return final_result
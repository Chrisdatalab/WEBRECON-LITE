from collections import deque
from urllib.parse import urlparse, urldefrag
from webrecon.extractor import link_extractor,js_extractor
from webrecon.utils import http_client
from webrecon.analyzer import link_analyzer, js_analyzer


def normalize_url(url):
    """
        Normalize URL to reduce duplicate crawling.
        Example:
        https://example.com/about#team -> https://example.com/about
    """
    url, _ = urldefrag(url)
    if url.endswith("/") and len(url) > len("https://"):
        return url.rstrip("/")
    else:
        return url

def get_host(url):
    """
        Extract the hostname from a URL.

        This is used to make sure the crawler only visits
        pages from the same target website and does not crawl
        external domains.
    """
    return urlparse(url).hostname

def crawler_source_http(source, depth=1, m_pages=20):
    visited = set()
    visited_order = []
    queued = set()
    pages = []

    source = normalize_url(source)
    target_host = get_host(source)

    q = deque()
    q.append((source, 0))
    queued.add(source)

    while q and len(visited) < m_pages:
        curr_link, current_depth = q.popleft()
        curr_link = normalize_url(curr_link)

        if curr_link in visited:
            continue

        parsed_curr = urlparse(curr_link)

        if parsed_curr.scheme not in ["http", "https"]:
            continue

        if get_host(curr_link) != target_host:
            continue

        r = http_client.http_get(curr_link)

        if r is None:
            continue

        visited.add(curr_link)
        visited_order.append(curr_link)

        result = link_extractor.extract_links(r, curr_link)
        javascript_result = js_extractor.extract_javascript(r.text,curr_link)
        links = result.get("links", [])

        link_analysis = link_analyzer.link_analysis(links,curr_link)
        
        javascript_analysis = js_analyzer.analyze_javascript(javascript_result,curr_link)
        result["url"] = curr_link
        result["depth"] = current_depth
        result["analysis"] = {
            "links": link_analysis,
            "javascript": {
                            "extracted": javascript_result,
                            "analysis": javascript_analysis
                        }
        }

        pages.append(result)

        if current_depth < depth:
            for new_link in links:
                new_link = normalize_url(new_link)
                parsed_new_link = urlparse(new_link)

                if parsed_new_link.scheme not in ["http", "https"]:
                    continue

                if get_host(new_link) != target_host:
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
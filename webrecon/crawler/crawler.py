from webrecon.extractor import link_extractor
from webrecon.utils import http_client
from webrecon.analyzer import link_analyzer
from collections import deque
from urllib.parse import urlparse


def crawler_source_http(source, depth, m_pages):
    visited = set()
    queued = set()
    pages = []

    target_domain = urlparse(source).netloc

    q = deque()
    q.append((source, 0))
    queued.add(source)

    while q and len(visited) < m_pages:
        curr_link, current_depth = q.popleft()

        if curr_link in visited:
            continue

        curr_domain = urlparse(curr_link).netloc

        if curr_domain != target_domain:
            continue

        r = http_client.http_get(curr_link)

        if r is None:
            continue

        visited.add(curr_link)

        result = link_extractor.extract_links(
            r,
            curr_link,
            depth,
            m_pages
        )

        link_analysis = link_analyzer.link_analysis(
            result["links"],
            curr_link
        )

        result["url"] = curr_link
        result["depth"] = current_depth
        result["analysis"] = {}
        result["analysis"]["links"] = link_analysis

        pages.append(result)

        if current_depth < depth:
            for new_link in result["links"]:
                parsed_new_link = urlparse(new_link)

                if parsed_new_link.scheme not in ["http", "https"]:
                    continue

                if parsed_new_link.netloc != target_domain:
                    continue

                if new_link not in visited and new_link not in queued:
                    q.append((new_link, current_depth + 1))
                    queued.add(new_link)

    final_result = {
        "target": source,
        "max_depth": depth,
        "max_pages": m_pages,
        "pages_crawled": len(pages),
        "visited_urls": list(visited),
        "pages": pages
    }

    return final_result
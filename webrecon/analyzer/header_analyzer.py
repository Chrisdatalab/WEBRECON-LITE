

def analyze_headers(headers, url):
    security_headers=(
                            "Strict-Transport-Security",
                            "Content-Security-Policy",
                            "X-Content-Type-Options",
                            "X-Frame-Options",
                            "Referrer-Policy",
                            "Permissions-Policy"
    )
    present_headers={}
    missing_headers=[]
    for head in security_headers:
        if head in headers:
            present_headers[head] = headers[head]
        else:
            missing_headers.append(head)

    return {
        "url": url,
        "present_headers": present_headers,
        "missing_headers": missing_headers
    }
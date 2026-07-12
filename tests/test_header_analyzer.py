from webrecon.analyzer.header_analyzer import analyze_headers

def test_some_security_headers_present():
    headers = {
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "DENY",
        "Server": "nginx"
    }
    url = "https://example.com"

    result = analyze_headers(headers, url)

    assert result["url"] == url

    assert result["present_headers"] == {
        "Content-Security-Policy": "default-src 'self'",
        "X-Frame-Options": "DENY"
    }

    assert "Strict-Transport-Security" in result["missing_headers"]
    assert "Permissions-Policy" in result["missing_headers"]

    assert "Server" not in result["present_headers"]
    assert len(result["missing_headers"]) == 4

def test_all_security_headers_present():
    headers = {
        "Strict-Transport-Security": "max-age=31536000",
        "Content-Security-Policy": "default-src 'self'",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "camera=()"
    }

    result = analyze_headers(headers, "https://example.com")

    assert len(result["present_headers"]) == 6
    assert result["missing_headers"] == []

def test_all_security_headers_missing():
    headers = {}

    result = analyze_headers(headers, "https://example.com")

    assert result["present_headers"] == {}
    assert len(result["missing_headers"]) == 6

    assert "Content-Security-Policy" in result["missing_headers"]
    assert "X-Frame-Options" in result["missing_headers"]
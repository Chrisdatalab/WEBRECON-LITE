from webrecon.analyzer.js_analyzer import analyze_javascript


def test_analyze_javascript():
    javascript_result = {
        "external_scripts": [
            "https://example.com/js/app.js",
            "https://example.com/js/app.min.js",
            "https://cdn.example.net/library.js?v=2",
            "http://cdn.example.net/old.min.js",
        ],
        "inline_scripts": [
            "console.log('hello');"
        ],
    }

    result = analyze_javascript(
        javascript_result,
        "https://example.com/home"
    )

    assert result["total_external_scripts"] == 4
    assert result["total_inline_scripts"] == 1

    assert result["internal_scripts"] == [
        "https://example.com/js/app.js",
        "https://example.com/js/app.min.js",
    ]

    assert result["third_party_scripts"] == [
        "https://cdn.example.net/library.js?v=2",
        "http://cdn.example.net/old.min.js",
    ]

    assert result["minified_scripts"] == [
        "https://example.com/js/app.min.js",
        "http://cdn.example.net/old.min.js",
    ]

    assert result["parameterized_scripts"] == [
        "https://cdn.example.net/library.js?v=2"
    ]

    assert result["insecure_scripts"] == [
        "http://cdn.example.net/old.min.js"
    ]
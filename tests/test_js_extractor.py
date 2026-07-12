from webrecon.extractor.js_extractor import extract_javascript


def test_extract_javascript():
    html = """
    <html>
        <head>
            <script src="/js/app.js"></script>

            <script src="https://example.com/js/app.js"></script>

            <script src="https://cdn.example.com/library.js"></script>

            <script>
                console.log("hello");
            </script>

            <script></script>
        </head>
    </html>
    """

    result = extract_javascript(
        html,
        "https://example.com/home"
    )

    assert result["external_scripts"] == [
        "https://example.com/js/app.js",
        "https://cdn.example.com/library.js",
    ]

    assert result["inline_scripts"] == [
        'console.log("hello");'
    ]
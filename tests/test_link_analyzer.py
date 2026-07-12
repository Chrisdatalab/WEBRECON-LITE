from webrecon.analyzer.link_analyzer import link_analysis


def test_link_analysis():
    links = [
        "https://example.com/about",
        "https://example.com/products?id=10",
        "https://example.com/admin",
        "https://example.com/files/report.pdf",
        "https://google.com",
        "mailto:admin@example.com",
    ]

    result = link_analysis(
        links,
        "https://example.com/home"
    )

    assert result["total_links"] == 6

    assert result["internal_links"] == [
        "https://example.com/about",
        "https://example.com/products?id=10",
        "https://example.com/admin",
        "https://example.com/files/report.pdf",
    ]

    assert result["external_links"] == [
        "https://google.com"
    ]

    assert result["document_files"] == [
        "https://example.com/files/report.pdf"
    ]

    assert result["login_or_admin_paths"] == [
        "https://example.com/admin"
    ]

    assert result["parameterized_links"] == [
        "https://example.com/products?id=10"
    ]

    print("All link analysis tests passed.")


test_link_analysis()
def test_non_web_links_are_ignored():
    links = [
        "mailto:admin@example.com",
        "tel:123456789",
        "javascript:void(0)",
    ]

    result = link_analysis(
        links,
        "https://example.com"
    )

    assert result["internal_links"] == []
    assert result["external_links"] == []


def test_uppercase_document_extension():
    links = [
        "https://example.com/files/REPORT.PDF"
    ]

    result = link_analysis(
        links,
        "https://example.com"
    )

    assert result["document_files"] == [
        "https://example.com/files/REPORT.PDF"
    ]
from webrecon.utils.url_utils import is_url_in_scope


def test_http_url_in_scope():
    assert is_url_in_scope(
        "http://example.com/page",
        "example.com"
    ) is True


def test_https_url_in_scope():
    assert is_url_in_scope(
        "https://example.com/page",
        "example.com"
    ) is True


def test_external_host_out_of_scope():
    assert is_url_in_scope(
        "https://external.com/page",
        "example.com"
    ) is False


def test_ftp_url_out_of_scope():
    assert is_url_in_scope(
        "ftp://example.com/file",
        "example.com"
    ) is False
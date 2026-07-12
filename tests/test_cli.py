from webrecon.cli import check_url, check_output_name


def test_valid_http_url():
    assert check_url("http://example.com") is True


def test_valid_https_url():
    assert check_url("https://example.com") is True


def test_url_without_scheme():
    assert check_url("example.com") is False


def test_invalid_scheme():
    assert check_url("ftp://example.com") is False


def test_missing_hostname():
    assert check_url("https://") is False


def test_url_with_space():
    assert check_url("https://example .com") is False
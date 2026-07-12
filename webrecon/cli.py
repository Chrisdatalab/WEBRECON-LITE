import argparse
from urllib.parse import urlparse

from webrecon.crawler import crawler
import webrecon.reporter.report_writer as reporter


def check_url(url):
    if not url or any(char.isspace() for char in url):
        return False

    try:
        parsed_url = urlparse(url)

        return (
            parsed_url.scheme.lower() in ("http", "https")
            and parsed_url.hostname is not None
        )
    except ValueError:
        return False


def check_output_name(name):
    if not name:
        return False

    allowed_symbols = {"-", "_"}

    for char in name:
        if not (
            char.isascii()
            and char.isalnum()
        ) and char not in allowed_symbols:
            return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="WebRecon-Lite web reconnaissance scanner"
    )

    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-o", "--output", default="report")
    parser.add_argument("-d", "--depth", type=int, default=2)
    parser.add_argument(
        "-m",
        "--max-pages",
        dest="max_pages",
        type=int,
        default=30
    )

    args = parser.parse_args()

    if not check_url(args.target):
        parser.error(
            "target must be a valid HTTP or HTTPS URL, "
            "for example: https://example.com"
        )

    if args.depth < 0:
        parser.error("depth must be 0 or greater")

    if args.max_pages < 1:
        parser.error("max-pages must be 1 or greater")

    if not check_output_name(args.output):
        parser.error(
            "output must contain only ASCII letters, numbers, "
            "hyphens, or underscores"
        )

    result = crawler.crawler_source_http(
        args.target,
        args.depth,
        args.max_pages
    )

    reporter.save_json_report(
        result,
        "output/reports/" + args.output + ".json"
    )

    reporter.print_report(result)
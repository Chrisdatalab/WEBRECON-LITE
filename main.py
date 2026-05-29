from webrecon.crawler import crawler
import webrecon.reporter.report_writer as reporter
import argparse

parse=argparse.ArgumentParser("")
parse.add_argument("-t", "--target")
args = parse.parse_args()
#source='https://books.toscrape.com/'
resolve=crawler.crawler_source_http(args.target)
reporter.print_report(resolve)
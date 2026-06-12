from webrecon.crawler import crawler
import webrecon.reporter.report_writer as reporter
import argparse
def check_URL(url):
    if url is None:
        return False
    if (url.startswith("http://") or url.startswith("https://"))and " " not in url:
        return True
    return False


parse=argparse.ArgumentParser("")
parse.add_argument("-t", "--target",required=True)
parse.add_argument('-o',"--output",default="report")
args = parse.parse_args()
#source='https://books.toscrape.com/'
if check_URL(args.target):
    result=crawler.crawler_source_http(args.target)
    reporter.save_json_report(result,"output/reports/"+args.output+".json")
else:
    result=None
reporter.print_report(result)
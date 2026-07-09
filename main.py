from webrecon.crawler import crawler
import webrecon.reporter.report_writer as reporter
import argparse
def check_URL(url):
    if url is None:
        return False
    if (url.startswith("http://") or url.startswith("https://"))and " " not in url:
        return True
    return False


parser=argparse.ArgumentParser("")
parser.add_argument("-t", "--target",required=True)
parser.add_argument('-o',"--output",default="report")
parser.add_argument("-d", "--depth", type=int, default=2)
parser.add_argument("-m", "--max-pages", dest="max_pages", type=int, default=30)

args = parser.parse_args()
#source='https://books.toscrape.com/'
if check_URL(args.target):
    result=crawler.crawler_source_http(args.target,args.depth,args.max_pages)
    reporter.save_json_report(result,"output/reports/"+args.output+".json")
else:
    result=None
reporter.print_summary(result)
#reporter.print_report(result)
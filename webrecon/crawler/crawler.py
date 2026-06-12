from webrecon.extractor import link_extractor
from webrecon.utils import http_client
from webrecon.analyzer import link_analyzer
def crawler_source_http(source):
    
    r=http_client.http_get(source)
    if r is not None:
        result=link_extractor.extract_links(r,source)
        link_analysis = link_analyzer.link_analysis(result["links"], source)
        result["analysis"] = {}
        result["analysis"]["links"] = link_analysis
        return result
    else:
        return None



    

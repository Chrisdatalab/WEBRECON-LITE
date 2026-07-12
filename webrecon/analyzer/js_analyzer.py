from urllib.parse import urlparse

def analyze_javascript(javascript_result, curr_link):

    external_script_urls = javascript_result.get("external_scripts",[])
    inline_scripts = javascript_result.get("inline_scripts",[])
    analysis = {
        "total_external_scripts": len(external_script_urls),
        "total_inline_scripts": len(inline_scripts),
        "internal_scripts": [],
        "third_party_scripts": [],
        "minified_scripts": [],
        "parameterized_scripts": [],
        "insecure_scripts": [],
    }
    current_page = urlparse(curr_link)
    current_host = current_page.hostname
    current_scheme = current_page.scheme.lower()
    for script_url in external_script_urls:
        parsed_script = urlparse(script_url)

        script_host = parsed_script.hostname
        script_scheme = parsed_script.scheme.lower()
        script_path = parsed_script.path.lower()

        if script_host == current_host:
            analysis["internal_scripts"].append(script_url)
        else:
            analysis["third_party_scripts"].append(script_url)

        if script_path.endswith(".min.js"):
            analysis["minified_scripts"].append(script_url)

        if parsed_script.query:
            analysis["parameterized_scripts"].append(script_url)

        if (current_scheme == "https" and script_scheme == "http"):
            analysis["insecure_scripts"].append(script_url)
    return analysis

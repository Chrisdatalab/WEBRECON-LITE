from urllib.parse import urlparse


DOCUMENT_EXTENSIONS = (
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".txt",
    ".csv",
)


LOGIN_ADMIN_PATTERNS = (
    "/login",
    "/signin",
    "/sign-in",
    "/admin",
    "/administrator",
    "/dashboard",
    "/auth",
    "/account",
)


def link_analysis(links, curr_link):
    current_host = urlparse(curr_link).hostname

    analysis = {
        "total_links": len(links),
        "internal_links": [],
        "external_links": [],
        "document_files": [],
        "login_or_admin_paths": [],
        "parameterized_links": [],
    }

    for link in links:
        parsed_link = urlparse(link)

        scheme = parsed_link.scheme.lower()
        link_host = parsed_link.hostname
        path = parsed_link.path.lower()

        # Ignore non-web links.
        if scheme not in ("http", "https"):
            continue

        # Classify links as internal or external.
        if link_host == current_host:
            analysis["internal_links"].append(link)
        else:
            analysis["external_links"].append(link)

        # Detect document files.
        if path.endswith(DOCUMENT_EXTENSIONS):
            analysis["document_files"].append(link)

        # Detect login, authentication, and admin paths.
        if any(pattern in path for pattern in LOGIN_ADMIN_PATTERNS):
            analysis["login_or_admin_paths"].append(link)

        # Detect URLs containing query parameters.
        if parsed_link.query:
            analysis["parameterized_links"].append(link)

    return analysis
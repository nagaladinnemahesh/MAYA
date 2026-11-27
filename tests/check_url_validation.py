from tools.web_tools import WebTools


web = WebTools()

test_urls = [
    "python.org",
    "https://github.com",
    "http://example.com",
    "docs.python.org/3/",
    "amazon.in",
    "javascript:alert(1)",
    "file:///C:/Windows",
    "ftp://example.com",
    "invalidwebsite",
    "https://",
    "https://user:password@example.com",
    "https://example.com:99999",
    "",
    "   "
]

print("\n--- URL validation tests ---")

for url in test_urls:
    result = web.validate_url(url)

    print(f"Input: {url!r}")
    print(f"Result: {result}")
    print()

print("\n--- Open valid website ---")
print(web.open_url("python.org"))

print("\n--- Reject invalid website ---")
print(web.open_url("javascript:alert(1)"))
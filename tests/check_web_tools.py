from tools.web_tools import WebTools


web = WebTools()

print("\n--- Test 1: Website resolution ---")
print(web.resolve_website("google"))

print("\n--- Test 2: Alias resolution ---")
print(web.resolve_website("git hub"))

print("\n--- Test 3: Case normalization ---")
print(web.resolve_website("YouTube"))

print("\n--- Test 4: Unknown website ---")
print(web.resolve_website("unknownwebsite"))

print("\n--- Test 5: Open Google ---")
print(web.open_website("google"))

print("\n--- Test 6: Open GitHub using alias ---")
print(web.open_website("git hub"))

print("\n--- Test 7: Reject unknown website ---")
print(web.open_website("unknownwebsite"))
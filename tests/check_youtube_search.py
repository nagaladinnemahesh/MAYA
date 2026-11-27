from tools.web_tools import WebTools


web = WebTools()

print("\n--- Test 1: Basic YouTube search ---")
print(web.search_youtube("Python tutorials"))

print("\n--- Test 2: Multi-word search ---")
print(web.search_youtube("Artificial intelligence explained"))

print("\n--- Test 3: Special characters ---")
print(web.search_youtube("C++ programming"))

print("\n--- Test 4: Empty query ---")
print(web.search_youtube(""))

print("\n--- Test 5: Whitespace-only query ---")
print(web.search_youtube("   "))
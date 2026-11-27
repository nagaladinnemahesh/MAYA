from tools.web_tools import WebTools


web = WebTools()

print("\n--- Test 1: Basic Google search ---")
print(web.search_google("Python tutorials"))

print("\n--- Test 2: Multi-word search ---")
print(web.search_google("AI engineering roadmap"))

print("\n--- Test 3: Special characters ---")
print(web.search_google("C++ programming"))

print("\n--- Test 4: Multiple special characters ---")
print(web.search_google("Python & JavaScript"))

print("\n--- Test 5: Empty search query ---")
print(web.search_google(""))

print("\n--- Test 6: Whitespace-only query ---")
print(web.search_google("   "))
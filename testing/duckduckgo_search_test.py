# %% Imports
from ddgs import DDGS
from pprint import pprint

# %% Test
results = DDGS().text("python programming", max_results=4)

href_list = []
for r in results:
    href_list.append(r["href"])
print(href_list)

# %% List comprehension method
#hrefs = [r["href"] for r in DDGS().text("python programming", max_results=3)]


# %% Testing Implementation
def get_search_query_links(search_queries: list[str]) -> dict:
    results = {}
    for query in search_queries:
        results[query] = [r["href"] for r in DDGS().text(query, max_results=4)]
    pprint(results)
    return results

test_queries = ["limits of nuclear energy", "risks associated with nuclear energy", "environmental impact of nuclear energy", "safety concerns in nuclear power plants", "disadvantages of nuclear energy production"]
get_search_query_links(test_queries)

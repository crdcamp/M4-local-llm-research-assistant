# %% Imports
from ddgs import DDGS

# %% Test
results = DDGS().text("python programming", max_results=4)

for r in results:
    print(r["href"])

# %% List comprehension method
hrefs = [r["href"] for r in DDGS().text("python programming", max_results=3)]

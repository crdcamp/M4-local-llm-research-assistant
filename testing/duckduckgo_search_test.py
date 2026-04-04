# %% Imports
from ddgs import DDGS

# %% Test
results = DDGS().text("python programming", max_results=4)

for r in results:
    print(r["href"])

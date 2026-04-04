# %% Imports
from ddgs import DDGS

# %% Test
results = DDGS().text("python programming", max_results=3)
print(results)

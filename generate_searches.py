# %% Imports
from llama_cpp import Llama
import os

# %% Define file paths
models_dir = "models"
llm = "gemma-7b-it.gguf"
os.makedirs(models_dir, exist_ok=True)

# %% Load model
model = Llama(
    model_path = f"{models_dir}/{llm}"
)

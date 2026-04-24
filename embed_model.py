# %% Imports
import os
import sys
from llama_cpp import Llama

# %% File paths
models_dir = "models"
summary_dir = "data/summary"

if not os.path.exists(models_dir):
    print("Error: `models` directory not found. Exiting")
    sys.exit(1)

if not os.path.exists(summary_dir):
    print("Error: `summary` directory not found. Exiting")

# %% Load embedding modfel
embed_model = Llama(
    model_path="models/Qwen3-Embedding-8B-Q8_0.gguf",
    embedding=True,
    verbose=True,
    n_ctx = 40960
)

# %% Read markdown file function
def read_md(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f
    return md_content


# DO NOT RUN THIS YET!!!
# Embed model with
def embed_model():
    for file in os.listdir(summary_dir)
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f
            embedding = llm.create_embedding(md_content)
            #vector = embedding["data"][0]["embedding"]

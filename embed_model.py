# %% Imports
import os
import sys
from llama_cpp import Llama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Ref:
# https://www.youtube.com/watch?v=gigip1Pxf88

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
    n_ctx = 40960,
)

# %% Splitting into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

for filename in os.listdir(summary_dir):
    filepath = os.path.join(summary_dir, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        documents = text_splitter.create_documents([text])

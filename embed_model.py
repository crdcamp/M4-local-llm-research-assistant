# %% Imports
from itertools import islice
import os
import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_cpp import Llama
import time
import chromadb

def chunk(arr_range, chunk_size):
    arr_range = iter(arr_range)
    return iter(lambda: list(islice(arr_range, chunk_size)), [])

# %% File paths
models_dir = "models"
summary_dir = "data/summary"

if not os.path.exists(models_dir):
    print("Error: `models` directory not found. Exiting")
    sys.exit(1)

if not os.path.exists(summary_dir):
    print("Error: `summary` directory not found. Exiting")

# https://www.youtube.com/watch?v=gigip1Pxf88
# %% Splitting into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

# %% Load embedding model
print("Loading embed model")
embed_model = Llama(
    model_path="models/Qwen3-Embedding-8B-Q4_K_M.gguf",
    embedding=True,
    verbose=False,
    n_ctx = 40960,
    n_batch=2048
)

# REDO THIS ENTIRELY
# FOCUS ON GETTING IT WORKING WITH ONE DOCUMENT
# BEFORE TRYING ALL OF THEM
# %% Embed
print("Embedding...")
for filename in os.listdir(summary_dir):
    filepath = os.path.join(summary_dir, filename)
    batch_size = 100
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

        documents = text_splitter.create_documents([text])
        documents_embeddings = []
        batches = list(chunk(documents, batch_size))

        for batch in batches:
            embeddings = embed_model.create_embedding([item.page_content for item in batch])
            documents_embeddings.extend(
                [
                    (document, embeddings['embedding'])
                    for document, embeddings in zip(batch, embeddings['data'])
                ]
            )

        all_text = [item.page_content for item in documents]

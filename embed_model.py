"""
THIS CODE WILL NOT WORK FOR NEWER MODELS.
YOU NEED TO USE LLAMA-SERVER INSTEAD (I know, you put a good amount of effort into this...)
"""

# %% Imports
from itertools import islice
import os
import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_cpp import Llama

# For later use (maybe, I think I'm moving to llama-server instead)
import chromadb
import time

from itertools import islice


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
    model_path="models/gte-Qwen2-7B-instruct-Q6_K.gguf",
    embedding=True,
    verbose=False,
    n_ctx=40960
)

# # %% Test embedding file setup
# test_file_path = "data/summary/httpsawsamazoncomwhatisvectordatabases.md"
# with open(test_file_path, 'r', encoding='utf-8') as test_file:
#     test_md_content = test_file.read()


# def chunk(arr_range, chunk_size):
#     arr_range = iter(arr_range)
#     return iter(lambda: list(islice(arr_range, chunk_size)), [])

# documents = text_splitter.create_documents([test_md_content])

# # Show some properties of what we've just created
# print(len(documents))
# print(type(documents))
# print(documents[1])


# %% Single input embedding test
#single_embed = embed_model.embed (documents[:1])

# %% Small test embedding
# So we're getting the same error here... hmmmmmm
# .embed seems to work with only one field at a time...

#embeddings = embed_model.embed (["Hello", "World"])

"""
For some reason, `create_embeddings()` is only accepting one entry, even though
it should be able to accept multiple.
I've found someone with a similar issue on GitHub: https://github.com/abetlen/llama-cpp-python/issues/2051

I think this might be an issue with using a newer model, but before we try that let's try the following
"""

# Revised approach
# We'll just loop through the documents and embed them one at a time instead
# documents_embeddings = []
# for doc in documents:
#     emb_result = embed_model.embed(doc.page_content)

"""
Welp looks like that isn't working either!

I'll tell you what: we're gonna try to embed Qwen3 8B ourselves and if
that still doesn't work.... we'll have to try a new model
"""

# %% Final test embedding
# batch_size = 200
# documents_embeddings = []
# batches = list(chunk(documents, batch_size))

# start = time.time()
# for batch in batches:
#     embeddings = embed_model.create_embedding([item.page_content for item in batch])
#     documents_embeddings.extend(
#         [
#             (document, embeddings['embedding'])
#             for document, embeddings in zip(batch, embeddings['data'])
#         ]
#     )
# end = time.time()

# all_text = [item.page_content for item in documents]
# char_per_sec = len(''.join(all_text) / (end-start))
# print(f"Time: {end-start:.2f} seconds / {char_per_sec:,.2f} chars/second")


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

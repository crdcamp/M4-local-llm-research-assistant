# Vector Database Overview

A vector database is a specialized type of database designed to store, index, and search high-dimensional vector representations of data known as embeddings. Unlike traditional databases that rely on exact matches, vector databases use similarity search techniques such as cosine similarity or Euclidean distance to find items that are semantically or visually similar.

## Example Code Using FAISS

This code uses FAISS to store 3 sample vectors and perform a similarity search using L2 distance. The `query_vector` is compared to all stored vectors, and the indices and distances of the top 2 most similar vectors are returned.

```python
Output:
Indices of closest vectors: [[0 1]]

Distances from query: [[0.0025 0.0325]]
```
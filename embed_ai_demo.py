# GENERATED FROM CLAUDE AS A GUIDELINE
# THIS IS TO ONLY BE USED AS REFERENCE

# %% Imports (add this)
from sentence_transformers import SentenceTransformer

# %% Load embedding model separately from Llama
def load_embedding_model():
    print("Loading embedding model...")
    embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    print("Embedding model loaded\n")
    return embed_model

# %% Chunk markdown on headers
def chunk_markdown(text: str, source: str) -> list[dict]:
    sections = re.split(r'(?=^#{1,6}\s)', text, flags=re.MULTILINE)
    chunks = []
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        lines = section.splitlines()
        title = lines[0].lstrip('#').strip() if lines[0].startswith('#') else f"chunk_{i}"
        chunks.append({
            "text": section,
            "metadata": {"source": source, "title": title, "chunk_index": i}
        })
    return chunks

# %% Build ChromaDB collection
def build_vector_db(embed_model):
    print("Building vector database...")
    start_time = time.perf_counter()

    client = chromadb.PersistentClient(path="data/chroma_db")
    try:
        client.delete_collection("research")
    except Exception:
        pass
    collection = client.create_collection(
        name="research",
        metadata={"hnsw:space": "cosine"}
    )

    all_chunks = []
    for filename in os.listdir(html_summary_dir):
        if not filename.endswith(".md"):
            continue
        with open(os.path.join(html_summary_dir, filename), 'r', encoding='utf-8') as f:
            text = f.read()
        all_chunks.extend(chunk_markdown(text, source=filename))

    if not all_chunks:
        print("No chunks found — did gather_info() run successfully?")
        return collection

    print(f"Embedding {len(all_chunks)} chunks...")
    texts = [c["text"] for c in all_chunks]

    # Encode all chunks in one batched call — much faster than one at a time
    embeddings = embed_model.encode(texts, batch_size=32, show_progress_bar=True).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[c["metadata"] for c in all_chunks],
        ids=[f"chunk_{i}" for i in range(len(all_chunks))]
    )

    total_time = time.perf_counter() - start_time
    print(f"Vector DB built in {total_time:.2f}s — {len(all_chunks)} chunks stored\n")
    times.append(total_time)
    return collection

# %% Query
def query_db(collection, embed_model, prompt: str, n_results: int = 5) -> list[dict]:
    query_embedding = embed_model.encode(prompt).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        hits.append({"text": doc, "metadata": meta, "distance": dist})
    return hits

# %% Entry point
gather_info()
embed_model = load_embedding_model()
collection = build_vector_db(embed_model)

hits = query_db(collection, embed_model, input_prompt)
for hit in hits:
    print(f"[{hit['distance']:.4f}] {hit['metadata']['title']} ({hit['metadata']['source']})")
    print(hit['text'][:200])
    print("---")

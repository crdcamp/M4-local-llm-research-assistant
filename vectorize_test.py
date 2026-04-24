import chromadb
from llama_cpp import Llama

# AI GENERATED. JUST FOR REFERENCE

# Two models: one for embedding, one for generation
embed_model = Llama(model_path="models/nomic-embed-text.gguf", embedding=True, verbose=False)
gen_model = Llama(model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf", n_ctx=32768, verbose=False, chat_format="chatml")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("research_docs")

def get_embedding(text: str) -> list[float]:
    return embed_model.embed(text)

def vectorize_results():
    for filename in os.listdir(html_summary_dir):
        file_path = os.path.join(html_summary_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Split on double newlines — works well for your markdown output
        chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

        collection.add(
            documents=chunks,
            embeddings=[get_embedding(c) for c in chunks],
            metadatas=[{"source": filename}] * len(chunks),
            ids=[f"{filename}_{i}" for i in range(len(chunks))]
        )
        os.remove(file_path)

def retrieve_and_answer(user_query: str) -> str:
    results = collection.query(
        query_embeddings=[get_embedding(user_query)],
        n_results=5
    )
    context = "\n\n".join(results["documents"][0])

    response = gen_model.create_chat_completion(
        messages=[
            {"role": "system", "content": f"Answer using this context:\n\n{context}"},
            {"role": "user", "content": user_query}
        ]
    )
    return response["choices"][0]["message"]["content"]

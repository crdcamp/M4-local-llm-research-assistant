# The General Idea

I primarily use AI for gathering information and speeding up the process of using a search engine. I believe it's up to the user to actually investigate the provided material, as I've had an LLM tell me the wrong info way too many times.

I don't like paying for AI subscriptions either (well... who does?), since now I have enough technical knowledge to not need all the tokens that a paid plan provides.

**So, this is kind of what lead me to this project:** The goal is to create a local LLM with enough provided tools to act as a "research assistant" (even though I'm not a huge fan of that phrase). The intention is to have a model that runs well locally on a Macbook M4 chip (the base 16 GB model). It will be used strictly for gathering information together, give a general idea of the provided info, and provide links to the information it gathered.

I might also look into implementing some code capabilities, but that is a problem for later.

To summarize, I'm trying to create an extremely scaled down version of [Perplexity](https://www.perplexity.ai/) that runs locally with low hardware requirements.

# The Models I'm Testing

* [bartowski/Qwen2.5-7B-Instruct-Q4_K_M.gguf](https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/blob/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf) (A Qwen model quantized down to 4 bits)
* [unsloth/gemma-4-26B-A4B-it-GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF) (A Gemma model quantized down to 3 bits)

# AI Overview Project Outline (because I don't feel like manually typing this)

## 1. Project Overview
A local AI application that combines web searching with temporary Retrieval-Augmented Generation (RAG) to provide accurate, fact-based answers using a local LLM (llama.cpp) and an in-memory vector store.

## 2. Phase 1: Search & Scrape (Refinement)
- [x] **Query Generation:** Use LLM to turn one user prompt into multiple search queries.
- [x] **Web Scraping:** Retrieve content from DuckDuckGo results.
- [ ] **Data Cleaning:** Direct processing of relevant text sections from HTML (BeautifulSoup).

## 3. Phase 3: RAG Implementation (The Core Goal)
- [ ] **Text Chunking:**
    - Break retrieved HTML/Text into smaller segments (500-1000 characters).
    - Use overlapping chunks to maintain context across boundaries.
- [ ] **In-Memory Vector Storage:**
    - **Tool:** `ChromaDB` (running in ephemeral/memory mode for this iteration).
    - **Goal:** Get the retrieval loop working for single sessions before moving to disk.
- [ ] **Local Embeddings:**
    - Use the existing `llama-cpp-python` instance (`model.create_embedding`) to vectorize text chunks without loading extra models.

## 4. Phase 4: Optimized Inference & Retrieval
- [ ] **Similarity Search:**
    - Query the in-memory store for the most relevant chunks based on the user's prompt.
- [ ] **Context Augmentation:**
    - Construct a prompt that injects retrieved chunks directly into the LLM's context.
- [ ] **KV Cache Management:**
    - Monitor and optimize RAM usage to keep context processing fast.

## 5. Phase 5: Infrastructure
- [ ] **FastAPI Integration:** Finalize server setup for JSON requests.
- [ ] **Resource Singleton:** Ensure the `Llama` model is initialized once and shared across all research tasks to prevent memory leaks.

## 6. Future Expansion (Post-RAG Success)
- [ ] **Persistent Cache:** Moving from in-memory to disk-based storage.
- [ ] **Resource Capping:** Implementing LRU (Least Recently Used) eviction for disk management.

## 7. Performance Targets
- **Model:** Qwen2.5-7B (Q4_K_M).
- **RAM Usage:** < 8GB total.
- **Outcome:** Verified "grounded" answers where the AI cites its retrieved sources.

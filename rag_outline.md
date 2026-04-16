# Project Outline: Local RAG Research Assistant (v2)

## 1. Project Overview
A local AI application that combines web searching with persistent Retrieval-Augmented Generation (RAG) to provide accurate, fact-based answers using a local LLM (llama.cpp) and a disk-based vector cache.

## 2. Phase 1: Search & Scrape (Refinement)
- [x] **Query Generation:** Use LLM to turn one user prompt into multiple search queries.
- [x] **Web Scraping:** Retrieve HTML from DuckDuckGo results.
- [x] **Markdown Conversion:** Clean HTML into readable markdown.
- [ ] **Scrape Management:** Implement a "Cache-First" check to see if a query has been answered recently before hitting the web.

## 3. Phase 2: RAG Implementation (The Vector Backbone)
- [ ] **Document Chunking:**
    - Use `RecursiveCharacterTextSplitter` (500-800 character chunks).
- [ ] **Persistent Vector Storage:**
    - **Tool:** `ChromaDB` using `PersistentClient`.
    - **Location:** `./research_cache` folder on local disk.
- [ ] **Local Embeddings:**
    - Utilize `llama-cpp-python`'s internal embedding function to maintain a single-model RAM footprint.

## 4. Phase 3: The "Persistent Cache" System (Requirement)
- [ ] **LRU Eviction Policy:** - Monitor database size or entry count.
    - Automatically delete Least Recently Used (LRU) data chunks once a specific limit is reached (e.g., 2GB or 50,000 chunks).
- [ ] **Staleness Logic:**
    - Add timestamps to metadata.
    - If data is older than 7 days, trigger a re-scrape for updated info.
- [ ] **Resource Capping:**
    - Ensure disk usage remains predictable and doesn't exceed user-defined limits.

## 5. Phase 4: Optimized Inference
- [ ] **Hybrid Retrieval:**
    - Search local cache first; if "confidence" score is low, trigger web search.
- [ ] **Context Injection:**
    - Dynamically inject the top-5 most relevant chunks into the system prompt.
- [ ] **KV Cache Quantization:**
    - Use `--cache-type-k q4_0` in llama-cpp to save RAM during long-context processing.

## 6. Phase 5: Infrastructure & UI
- [ ] **FastAPI & WebSockets:** Enable real-time streaming of research results.
- [ ] **State Management:** Ensure the LLM model is loaded as a singleton to prevent double-loading in RAM.

## 7. Performance Targets
- **Model:** Qwen2.5-7B (Q4_K_M).
- **RAM Usage:** < 8GB (Inference) + < 1GB (Cache/DB).
- **Disk Usage:** Capped at 2GB for the Research Cache.

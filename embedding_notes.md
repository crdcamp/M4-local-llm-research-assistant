# Embedding Notes

The starting point for these notes can be found [here](https://github.com/ggml-org/llama.cpp/tree/master/tools/server).

An embedding example can be found [here](https://github.com/ggml-org/llama.cpp/discussions/7712).

Let's begin.

# Relevant Embedding Commands

`--pooling {none,mean,cls,last,rank}`

pooling type for embeddings, **use model default if unspecified**
(env: LLAMA_ARG_POOLING)

`--embedding, --embeddings` 

restrict to only support embedding use case; **use only with dedicated embedding models** (default: disabled)
(env: LLAMA_ARG_EMBEDDINGS)

`--embd-gemma-default`

use default EmbeddingGemma model (note: can download weights from the internet)

# Example Commands

```terminal
llama-embedding -m models/embed_models/Qwen3-Embedding-8B-Q6_K.gguf -e -p "Hello World" --verbose-prompt -ngl 99
```

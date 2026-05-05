#!/usr/bin/env bash

TARGET_MODEL="Qwen3-Embedding-8B-Q6_K.gguf"

MODELS_DIR="/models/"
EMBED_MODEL_DIR="models/embed_models/"
EMBED_DOCS=$(ls "data/summary"/*)

echo -e "DOCUMENTS TO EMBED:\n$EMBED_DOCS\n"

for model in "$EMBED_MODEL_DIR"*; do
    if [[ "$model" == *"$TARGET_MODEL" ]]; then
        TARGET_MODEL_DIR="$EMBED_MODEL_DIR$TARGET_MODEL"
        echo -e "TARGET MODEL FOUND: $TARGET_MODEL_DIR\nEmbedding...\n"


    else
        echo "MODEL NOT FOUND"
    fi
done

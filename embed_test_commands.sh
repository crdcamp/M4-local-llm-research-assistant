#!/usr/bin/env bash

SUMMARY_DIR="data/summary/"
MODELS_DIR="/models/"
EMBED_DIR="models/embed_models/"

echo "SUMMARY DIR: $SUMMARY_DIR"
echo "MODELS DIR: $MODELS_DIR"
echo -e "EMBED MODELS DIR: $EMBED_DIR\n"

for model in "$EMBED_DIR"*; do
    if [[ "$model" == *"Qwen3-Embedding-8B-Q6_K.gguf" ]]; then
        echo "MODEL FOUND: $EMBED_DIR/$model"
    else
        echo "Model not found"
    fi
done

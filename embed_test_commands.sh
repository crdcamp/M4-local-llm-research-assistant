#!/usr/bin/env bash

TARGET_MODEL="Qwen3-Embedding-8B-Q6_K.gguf"

SUMMARY_DIR="data/summary/"
MODELS_DIR="/models/"
EMBED_DIR="models/embed_models/"

echo "SUMMARY DIR: $SUMMARY_DIR"
echo "MODELS DIR: $MODELS_DIR"
echo -e "EMBED MODELS DIR: $EMBED_DIR\n"

for model in "$EMBED_DIR"*; do
    if [[ "$model" == *"$TARGET_MODEL" ]]; then
        TARGET_MODEL_DIR="$EMBED_DIR$TARGET_MODEL"
        echo -e "MODEL FOUND: $TARGET_MODEL_DIR\n"
    else
        echo "MODEL NOT FOUND\n"
    fi
done

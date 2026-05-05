#!/usr/bin/env bash

SUMMARY_DIR="data/summary/"
MODELS_DIR="/models/"
EMBED_DIR="models/embed_models/"

echo "Summary directory: $SUMMARY_DIR"
echo "Models directory: $MODELS_DIR"
echo -e "Embed models directory: $EMBED_DIR\n"

for model in "$EMBED_DIR"*; do
    echo "$model"
done

ls "$EMBED_DIR"

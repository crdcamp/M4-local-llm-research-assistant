import os
import sys
import chromadb
from llama_cpp import Llama

models_dir = "models"
summary_dir = "data/summary"
embed_model = f"{models_dir}/Qwen3-Embedding-8B-Q8_0.gguf"

if not os.path.exists(models_dir):
    print("Error: `models` directory not found. Exiting")
    sys.exit(1)

if not os.path.exists(summary_dir):
    print("Error: `summary` directory not found. Exiting")

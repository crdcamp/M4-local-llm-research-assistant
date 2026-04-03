# %% Imports
from llama_cpp import Llama
import os

# CONCLUSION: Qwen (assuming it can be used for tool calling) is unecessary for search generation
# Mistral will do this instead

# %% Define file paths and model parameters
models_dir = "../models"

# Models
mistral_7b_Q4 = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
qwen_7B_I_Q4 = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"

os.makedirs(models_dir, exist_ok=True)

# %% Load Models
test_prompt = "Provide me 5 internet searches to to help me find out the difference between endothermic and exothermic processes"

chat_mistral_7b_Q4 = Llama(
    model_path=f"{models_dir}/{llm_mistral_7b_4Q}",
    max_tokens=1024,
    chat_format="llama-2"
)

chat_qwen_7b_Q4 = Llama(
    model_path=f"{models_dir}/{qwen_7B_I_Q4}",
    max_tokens=1024,
    chat_format="llama-2"
)


# %% Generate searches for Mistral
print(chat_mistral_7b_Q4.create_chat_completion(
    messages=[{
        "role": "user",
        "content": test_prompt
    }]
))

# %% Generate searches for Qwen
print(chat_qwen_7b_Q4.create_chat_completion(
    messages=[{
        "role": "user",
        "content": test_prompt
    }]
))

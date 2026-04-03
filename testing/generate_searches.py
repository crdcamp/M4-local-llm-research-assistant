# %% Imports
from llama_cpp import Llama
import os

# %% Define file paths and model parameters
models_dir = "../models"
llm_mistral_7b_4Q = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
os.makedirs(models_dir, exist_ok=True)

# %% Load Model
test_prompt = "Provide me 5 internet searches to to help me find out the difference between endothermic and exothermic processes"

model_mistral_7b = Llama(
    model_path=f"{models_dir}/{llm_mistral_7b_4Q}",
    max_tokens=1024,
    chat_format="llama-2"
)

# %% Generate searches
print(model_mistral_7b.create_chat_completion(
    messages=[{
        "role": "user",
        "content": test_prompt
    }]
))

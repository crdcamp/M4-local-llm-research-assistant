# %% Imports
from llama_cpp import Llama
import os

# %% Define file paths
models_dir = "models"
llm_qwen = "Qwen3-8B-Q8_0.gguf"
llm_glm_9B_8bit = "GLM-4.6V-Flash-GGUF"
os.makedirs(models_dir, exist_ok=True)

# %% Load model
# Link to model: https://huggingface.co/Qwen/Qwen3-8B-GGUF/blob/main/Qwen3-8B-Q8_0.gguf
model = Llama(
    model_path = f"{models_dir}/{llm_qwen}",
)

# %% Testing to see if the model works
print(model.create_chat_completion(
     messages=[{
         "role": "user",
         "content": "What is the meaning of life?"
     }]
))

# %% Test initial response for requesting multiple search options
# Add more context window. Default isn't doing it
print(model.create_chat_completion(
    messages=[{
        "role": "user",
        "content": "Provide me 5 short internet searches to help find out the difference between endothermic and exothermic processes"
    }]
))

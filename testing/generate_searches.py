# %% Imports
from llama_cpp import Llama
import os

# %% Define file paths and model parameters
models_dir = "../models"
llm_qwen = "Qwen3-8B-Q8_0.gguf"
llm_glm_9B_8bit = "GLM-4.6V-Flash-Q8_0.gguf"
os.makedirs(models_dir, exist_ok=True)

# %% Define parameters and load models
# Links to models can be found in README
max_tokens = 4096
test_prompt = "Provide me 5 short internet searches to help find out the difference between endothermic and exothermic processes /no_think"

model_qwen = Llama(
    model_path=f"{models_dir}/{llm_qwen}",
    max_tokens=max_tokens
)
model_glm = Llama(
    model_path=f"{models_dir}/{llm_glm_9B_8bit}",
    max_tokens=max_tokens
)


# %% Qwen Test
print(model_qwen.create_chat_completion(
    messages=[{
        "role": "user",
        "content": test_prompt
    }]
))

# %% GLM Test
print(model_glm.create_chat_completion(
     messages=[{
         "role": "user",
         "content": test_prompt
     }]
))

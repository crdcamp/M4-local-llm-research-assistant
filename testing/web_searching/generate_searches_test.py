# %% Imports
from llama_cpp import Llama
import os

"""
CONCLUSION:
    I think Qwen might be the only model needed if I can get it to focus enough through system prompts
    and chat templates. Given that the system prompt can be used to narrow down the output and limit
    token usage, I see no point in using Mistral at all.
"""

# %% Define file paths and model parameters
models_dir = "../models"

# Models
mistral_7b_Q4 = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
qwen_7B_I_Q4 = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"

os.makedirs(models_dir, exist_ok=True)

# %% Define Parameters, and Load Models

# Parameters
system_prompt = "You are a search query generator. When given a question or topic, output exactly five concise search engine queries a person could enter into a browser to research it. Format your response as a numbered list (1-5) with one query per line. Output only the numbered list — no preamble, explanation, or commentary."

user_prompt_no_sys = "Provide me 5 internet searches to to help me find out the difference between endothermic and exothermic processes"
user_prompt_sys = "What is the difference between endothermic and exothermic processes?"

param_max_tokens = 1024
param_verbose = True
param_chat_format = "llama-2"

# Load models
chat_mistral_7b_Q4 = Llama(
    model_path=f"{models_dir}/{mistral_7b_Q4}",
    max_tokens=param_max_tokens,
    verbose=param_verbose,
    chat_format=param_chat_format
)

chat_qwen_7b_Q4 = Llama(
    model_path=f"{models_dir}/{qwen_7B_I_Q4}",
    max_tokens=param_max_tokens,
    verbose=param_verbose,
    chat_format="chatml"
)


"""
SIMPLE TESTS:
    Just seeing if things are running smoothly. We'll add system prompts and chat
    templates later.
""";

# %% Generate searches for Mistral
print(chat_mistral_7b_Q4.create_chat_completion(
    messages=[{
        "role": "user",
        "content": user_prompt_no_sys
    }]
))

# %% Generate searches for Qwen
print(chat_qwen_7b_Q4.create_chat_completion(
    messages=[{
        "role": "user",
        "content": user_prompt_no_sys
    }]
))

"""
ADDING SYSTEM PROMPTS:
    Now let's add system prompts to see if this improves the results at all
""";

# %% Generate searches with Mistral with system prompt
print(chat_mistral_7b_Q4.create_chat_completion(
    messages=[
        {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt_sys
    }
    ]
))

# %% Generate searches with Qwen with system prompt
print(chat_qwen_7b_Q4.create_chat_completion(
    messages=[
        {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt_sys
    }
    ]
))

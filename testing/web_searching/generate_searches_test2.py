# %% Imports
from llama_cpp import Llama
import os

"""
Now we're gonna test using only Qwen, since it's looking like using multiple models might be unnecessary.
I'll also need to look into quantizing Qwen on my own, or research further into better models.

For now (assuming this quantized version of Qwen can call tools)... this will do.
""";

# %% File paths and model
models_dir = "../models"
qwen_7B_I_Q4 = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"
os.makedirs(models_dir, exist_ok=True)

# %% Define Parameters
system_prompt = "You are a search query generator. When given a question or topic, output exactly five concise search engine queries a person could enter into a browser to research it. Format your response as a numbered list (1-5) with one query per line. Output only the numbered list — no preamble, explanation, or commentary."
system_prompt_no_lim = "You are a search query generator. When given a question or topic, output several relevant and concise search engine queries a person could enter into a browser to research it. Format your response as a numbered list with one query per line. Output only the numbered list — no preamble, explanation, or commentary."

user_prompt_no_sys = "Provide me 5 internet searches to to help me find out the difference between endothermic and exothermic processes"
user_prompt_sys = "What is the difference between endothermic and exothermic processes?"

param_max_tokens = 1024
param_verbose = True
param_chat_format = "chatml"

# %% Load model
chat_qwen_7b_Q4 = Llama(
    model_path=f"{models_dir}/{qwen_7B_I_Q4}",
    max_tokens=param_max_tokens,
    verbose=param_verbose,
    chat_format=param_chat_format
)

# %% Generate searches without system prompt
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

# %% Generate searches with system prompt
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

# %% Generate searches with alternative system prompt (no search number limit)
print(chat_qwen_7b_Q4.create_chat_completion(
    messages=[
        {
        "role": "system",
        "content": system_prompt_no_lim
    },
    {
        "role": "user",
        "content": user_prompt_sys
    }
    ]
))

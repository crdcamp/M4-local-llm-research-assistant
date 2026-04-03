# %% Imports
from mcp.server import FastMCP
from llama_cpp import Llama

# %% Create MCP server
mcp = FastMCP("Research Assistant")

# %% Define Tools
@mcp.tool()
def generate_search_queries(user_prompt: str) -> str:
    """Output exactly five concise search engine queries a person could enter into a browser to research it"""
    model = Llama(
        model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
        max_tokens=1024,
        verbose=False,
        chat_format="chatml"
    )

    response = model.create_chat_completion(
        messages=[
            {
            "role": "system",
            "content": "You are a search query generator. When given a question or topic, output exactly five concise search engine queries a person could enter into a browser to research it. Format your response as a numbered list (1-5) with one query per line. Output only the numbered list — no preamble, explanation, or commentary."
        },
        {
            "role": "user",
            "content": user_prompt
        }]
    )

    return response["choices"][0]["message"]["content"]

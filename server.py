from mcp.server import FastMCP
from llama_cpp import Llama

# Create MCP server
mcp = FastMCP("Research Assistant")

# Load model
# THIS SHOULD PROBABLY GO IN `main.py`
model = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    max_tokens=2048,
    verbose=False,
    chat_format="chatml"
)

@mcp.tool()
# This needs to be adjusted to be output as a Python list...
def generate_search_queries(user_prompt: str) -> str:
    """Generate five targeted search enginew queries to research a given topic or question. Use this tool when you need to find information on the web about a specific subject."""

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

# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")

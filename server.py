from mcp.server import FastMCP
from llama_cpp import Llama
from pydantic import BaseModel
import json

mcp = FastMCP("Research Assistant")

model = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    max_tokens=2048,
    verbose=False,
    chat_format="chatml"
)

class SearchQueries(BaseModel):
    queries: list[str]

@mcp.tool()
def generate_search_queries(user_prompt: str) -> list[str]:
    """Generate five targeted search engine queries to research a given topic or question."""

    response = model.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a search query generator. When given a question or topic, generate exactly five concise search engine queries a person could enter into a browser to research it."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format={
            "type": "json_object",
            "schema": SearchQueries.model_json_schema()
        }
    )

    content = response["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    return parsed["queries"]

if __name__ == "__main__":
    mcp.run(transport="stdio")

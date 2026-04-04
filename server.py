from mcp.server import FastMCP
from llama_cpp import Llama
from pydantic import BaseModel
import json
from ddgs import DDGS

mcp = FastMCP("Research Assistant")

print("Loading model...")
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

@mcp.tool()
# CHANGE TO LIST COMPREHENSION METHOD
# PROBABLY SHOULD RENAME THIS TO GET_LINKS OR SOMETHING LIKE THAT
def search_the_internet(search_input: str):
    """ADD DESCRIPTION HERE"""
    results = DDGS().text(search_input, max_results=4)

    links = []
    for r in results:
        links.append(r["href"])

    return links

if __name__ == "__main__":
    mcp.run(transport="stdio")

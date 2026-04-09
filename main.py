from fastapi import FastAPI, WebSocket
from llama_cpp import Llama
from pydantic import BaseModel
import json
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from starlette.responses import HTMLResponse

"""
NOTES
* Warning when loading model: llama_context: n_ctx_seq (512) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
* Function descriptions could use a lot more work
* Look into properly loading the model: https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#core-concepts
    * When looking at Activity Monitor, it looks like the model might be loaded twice
"""

app = FastAPI()

html = """
<!doctype html>

<html class="light" lang="en">
    <head>
        <meta charset="utf-8" />
        <meta content="width=device-width, initial-scale=1.0" name="viewport" />
        <title>Manuscript</title>
        <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
        <link
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap"
            rel="stylesheet"
        />
        <link
            href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap"
            rel="stylesheet"
        />
        <link
            href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap"
            rel="stylesheet"
        />
        <script id="tailwind-config">
            tailwind.config = {
                darkMode: "class",
                theme: {
                    extend: {
                        colors: {
                            "on-tertiary": "#e2e2e2",
                            "on-primary-container": "#ffffff",
                            "surface-container-low": "#f3f3f4",
                            "surface-container": "#eeeeee",
                            "on-secondary": "#ffffff",
                            "surface-tint": "#5e5e5e",
                            "secondary-fixed": "#c8c6c6",
                            error: "#ba1a1a",
                            "on-background": "#1a1c1c",
                            primary: "#000000",
                            "on-tertiary-fixed": "#ffffff",
                            "primary-container": "#3b3b3b",
                            "on-secondary-fixed-variant": "#3b3b3b",
                            "surface-dim": "#dadada",
                            "on-error": "#ffffff",
                            "inverse-primary": "#c6c6c6",
                            "surface-container-highest": "#e2e2e2",
                            "surface-variant": "#e2e2e2",
                            "secondary-fixed-dim": "#acabab",
                            "on-error-container": "#410002",
                            "inverse-on-surface": "#f0f1f1",
                            secondary: "#5f5e5e",
                            surface: "#f9f9f9",
                            "on-primary-fixed-variant": "#e2e2e2",
                            "error-container": "#ffdad6",
                            "primary-fixed": "#5e5e5e",
                            "on-secondary-fixed": "#1b1c1c",
                            "on-tertiary-container": "#ffffff",
                            "primary-fixed-dim": "#474747",
                            "tertiary-container": "#747474",
                            "surface-bright": "#f9f9f9",
                            tertiary: "#3b3b3b",
                            "on-secondary-container": "#1b1c1c",
                            "on-surface-variant": "#474747",
                            "inverse-surface": "#2f3131",
                            background: "#f9f9f9",
                            "tertiary-fixed": "#5e5e5e",
                            "on-primary-fixed": "#ffffff",
                            outline: "#777777",
                            "outline-variant": "#c6c6c6",
                            "tertiary-fixed-dim": "#474747",
                            "surface-container-lowest": "#ffffff",
                            "surface-container-high": "#e8e8e8",
                            "secondary-container": "#d6d4d3",
                            "on-surface": "#1a1c1c",
                            "on-primary": "#e2e2e2",
                            "on-tertiary-fixed-variant": "#e2e2e2",
                        },
                        borderRadius: {
                            DEFAULT: "0px",
                            lg: "0px",
                            xl: "0px",
                            full: "0px",
                        },
                        fontFamily: {
                            headline: ["Inter"],
                            body: ["Inter"],
                            label: ["Inter"],
                        },
                    },
                },
            };
        </script>
        <style>
            body {
                font-family: "Inter", sans-serif;
            }
            .material-symbols-outlined {
                font-variation-settings:
                    "FILL" 0,
                    "wght" 400,
                    "GRAD" 0,
                    "opsz" 24;
            }
            /* Custom scrollbar for minimalism */
            #chat-container::-webkit-scrollbar {
                width: 4px;
            }
            #chat-container::-webkit-scrollbar-track {
                background: transparent;
            }
            #chat-container::-webkit-scrollbar-thumb {
                background: #e2e2e2;
            }
        </style>
    </head>
    <body
        class="bg-surface text-on-surface min-h-screen flex flex-col items-center"
    >
        <!-- Top Navigation Anchor -->
        <header
            class="bg-neutral-50 dark:bg-neutral-950 flex justify-between items-center w-full px-6 py-4 max-w-none fixed top-0 z-50"
        >
            <div
                class="text-xl font-bold text-black dark:text-white tracking-tighter"
            >
                Manuscript
            </div>
            <div class="flex gap-8">
                <span
                    class="font-inter tracking-tighter text-lg text-black dark:text-white font-semibold cursor-pointer transition-all duration-200 ease-in-out"
                    >Chat</span
                >
            </div>
        </header>
        <!-- Main Content Canvas -->
        <main class="w-full max-w-4xl flex-grow flex flex-col pt-20 pb-32 px-6">
            <!-- Chat Area -->
            <div
                class="flex flex-col space-y-12 overflow-y-auto flex-grow h-[calc(100vh-250px)]"
                id="chat-container"
            >
                <!-- Messages will be appended here -->
                <!-- AI Message Example Structure -->
                <div class="ai-message text-left max-w-2xl group">
                    <div class="text-on-surface leading-relaxed text-lg">
                        Manuscript initialization complete.
                    </div>
                    <div
                        class="text-[0.6875rem] text-on-surface-variant mt-2 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        Just now
                    </div>
                </div>
                <!-- User Message Example Structure -->
                <div class="user-message text-left max-w-2xl ml-auto group">
                    <div
                        class="text-on-surface font-semibold leading-relaxed text-lg"
                    >
                        Ready to begin.
                    </div>
                    <div
                        class="text-[0.6875rem] text-on-surface-variant mt-2 text-right opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        Just now
                    </div>
                </div>
            </div>
        </main>
        <!-- Input Zone -->
        <footer
            class="fixed bottom-0 left-0 w-full bg-surface-container-lowest p-6 flex justify-center"
        >
            <div class="w-full max-w-4xl relative">
                <div
                    class="flex items-end border border-outline-variant border-opacity-15 focus-within:border-opacity-40 transition-all duration-300 bg-surface-container-lowest"
                >
                    <textarea
                        class="w-full bg-transparent border-none focus:ring-0 resize-none py-4 px-6 text-lg placeholder-on-surface-variant/50"
                        id="message-input"
                        placeholder="Send a message..."
                        rows="1"
                    ></textarea>
                    <button
                        class="bg-primary text-on-primary p-4 hover:opacity-70 transition-opacity flex items-center justify-center"
                        id="send-button"
                    >
                        <span
                            class="material-symbols-outlined"
                            data-icon="north"
                            >north</span
                        >
                    </button>
                </div>
            </div>
        </footer>
        <!-- WebSocket Integration Script Template -->
        <script>
            const chatContainer = document.getElementById("chat-container");
            const messageInput = document.getElementById("message-input");
            const sendButton = document.getElementById("send-button");

            // Note: Replace with your actual FastAPI WebSocket endpoint
            const socket = new WebSocket(`ws://${window.location.host}/ws`);

            function appendMessage(text, role) {
                const wrapper = document.createElement("div");
                const isUser = role === "user";

                wrapper.className = isUser
                    ? "user-message text-left max-w-2xl ml-auto group"
                    : "ai-message text-left max-w-2xl group";

                const contentClass = isUser
                    ? "text-on-surface font-semibold leading-relaxed text-lg"
                    : "text-on-surface leading-relaxed text-lg";

                wrapper.innerHTML = `
                <div class="${contentClass}">${text}</div>
                <div class="text-[0.6875rem] text-on-surface-variant mt-2 ${isUser ? "text-right" : ""} opacity-0 group-hover:opacity-100 transition-opacity">Just now</div>
            `;

                chatContainer.appendChild(wrapper);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function handleSend() {
                const message = messageInput.value.trim();
                if (message) {
                    appendMessage(message, "user");
                    socket.send(message); // WebSocket execution
                    messageInput.value = "";
                    messageInput.style.height = "auto";
                }
            }

            sendButton.addEventListener("click", handleSend);

            messageInput.addEventListener("keydown", (e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                }
            });

            // Auto-resize textarea
            messageInput.addEventListener("input", function () {
                this.style.height = "auto";
                this.style.height = this.scrollHeight + "px";
            });

            // WebSocket Event Listeners Example
        socket.onmessage = function(event) {
            appendMessage(event.data, 'ai');
        };

        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = research_tool(data)
        await websocket.send_text(result)

print("Loading model...")
model = Llama(
    model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    n_ctx = 2048,
    max_tokens=2048,
    verbose=False,
    chat_format="chatml"
)

# Structured list output for `generate_search_queries`
class SearchQueries(BaseModel):
    queries: list[str]

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

def get_search_query_links(search_queries: list[str]) -> dict:
    """Takes a list of search queries and returns a dict mapping each query to a list of URLs resulting from the search query."""
    query_url_dict = {}
    for query in search_queries:
        query_url_dict[query] = [r["href"] for r in DDGS().text(query, max_results=4)]

    return query_url_dict


def convert_html_to_markdown(query_url_dict: dict) -> dict:
    """Retrieves HTML content from a given URL, strips the HTML content, and converts to markdown"""
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    STRIP_TAGS = ['script', 'style', 'nav', 'header', 'footer', 'aside',
                    'noscript', 'iframe', 'form', 'button', 'svg', 'figure',
                    'advertisement', 'cookie-banner']

    md_results = {}

    for query, urls in query_url_dict.items():
        md_results[query] = {}

        for url in urls:
            try:
                r = requests.get(url, headers=HEADERS, timeout=7)
                soup = BeautifulSoup(r.text, 'html.parser')
                for tag in soup(STRIP_TAGS):
                    tag.decompose()

                main = soup.find('main') or soup.find('article') or soup.find(id='content') or soup.find(class_='content') or soup.body
                clean_html = str(main) if main else str(soup)

                md_results[query][url] = md(clean_html, strip=['a', 'img'])

            except Exception as e:
                print(f"Error fetching {url}: {e}")

    return md_results

def interpret_md_results(markdown_results: dict) -> str:
    # We'll just start by accessing one entry.
    # Keep it simple for testing for now

    for query, url_dict in markdown_results.items():
        first_url = next(iter(url_dict))
        content = url_dict[first_url]

        response = model.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Summarize the following web page content clearly and concisely, focusing on the most relevant facts and key points. Ignore navigation text, ads, or other boilerplate."
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        return response["choices"][0]["message"]["content"]

def research_tool(prompt: str) -> dict:
    """Search the web and return page content as markdown for a given research prompt."""
    search_queries_list = generate_search_queries(prompt)
    search_queries_dict = get_search_query_links(search_queries_list)
    url_md_results = convert_html_to_markdown(search_queries_dict)
    chat_response = interpret_md_results(url_md_results)

    return chat_response

# The General Idea

I primarily use AI for gathering information and speeding up the process of using a search engine. I believe it's up to the user to actually investigate the provided material, as I've had an LLM tell me the wrong info way too many times.

I don't like paying for AI subscriptions either (well... who does?), since now that I've gained enough understanding of coding to the point where I don't need all the tokens that a paid plan provides.

**So, this is kind of what lead me to this project:** The goal is to create a local LLM with enough provided tools to act as a "research assistant" (even though I'm not a huge fan of that phrase). The intention is to have a model that runs well locally on a Macbook M4 chip (the base 16 gig model). It will be used strictly for gathering information together, give a general idea of the provided info, and provide links to the information it gathered.

To summarize, I'm trying to create an extremely scaled down version of [Perplexity](https://www.perplexity.ai/) that runs locally with low hardware requirements.

# The Model I'm Using

* [bartowski/Qwen2.5-7B-Instruct-Q4_K_M.gguf](https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/blob/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf) (A Qwen model quantized down to 4 bits)

# The Process

While I've touched on the relevant material for making something like this happen in the past, it wasn't until now that I've actually thought of a way to make this work and be legitimately useful. So, here's how we're gonna structure it:

## llama.cpp

[llama.cpp](https://github.com/ggml-org/llama.cpp) is the entry point for this project. It requires models to be stored in a [GGUF](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) file format, which enables fast loading and saving of models. Essentially, it's just a way to get these models running a bit more smoothly in the Python scripts.

[llama.cpp](https://github.com/ggml-org/llama.cpp) also has [`llama-cli`](https://github.com/ggml-org/llama.cpp?tab=readme-ov-file#llama-cli) which can be used for experimenting with these models. So, I won't have to make any sort of interface for testing or mess around with code too much once I get this set up.

Moreover, you can also [quantize models](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md), which reduces the precision of their weights which also requires less computational demand (I'm sure I'm leaving out many technical details here but that's the general idea). I can play around with this if needed, but I'm hoping I won't need to.

I also believe (I'll have to confirm this later) that I can have this project run in a web page with a nice interface. But, that's a problem I'll have to get to and sort out later.

Finally, [llama.cpp](https://github.com/ggml-org/llama.cpp) has a lot of options for playing around with the model's interaction with the hardware, so (with enough research), I'll have a lot of ways to make things run more smoothly when the general structure is complete.

## Workflow Outline

- [x] Give an input prompt (a research question)
- [x] Generate 5 internet search queries to execute for input prompt
- [x] From these 5 internet search queries, retrieve the top 4 URLs
- [ ] Retrieve the HTML content from each URL and convert to markdown
- [ ] Have LLM interpret the markdown results and provide links for each summary (might need to add additional steps for this one)

If the local LLMs can't generate good google searches, then we might have to look into training them with the Claude API. Before then, we'll just get this general workflow working and fine tune everything after the initial structure is ready.

# Some Notes for Me

## General

* [MCP Course](https://huggingface.co/learn/mcp-course/unit0/introduction)
* [Introduction to creating MCP server](https://www.youtube.com/watch?v=exzrb5QNUis)

## Getting Started with [`uv`](https://github.com/astral-sh/uv)

```terminal
uv venv
source .venv/bin/activate
uv pip install "mcp[cli]" llama-cpp-python
```

## Running MCP with `dev` Command

```terminal
mcp dev server.py
```

## Installing `requirements.txt` with `uv`

To [import dependencies from `requirements.txt` file:](*https://docs.astral.sh/uv/concepts/projects/dependencies/#importing-dependencies-from-requirements-files)

```terminal
uv add -r requirements.txt
```

See the [pip migration guide](https://docs.astral.sh/uv/guides/migration/pip-to-project/#importing-requirements-files) for more details.

## Use [Sampling](https://huggingface.co/learn/mcp-course/unit1/capabilities#sampling) to Define Full Workflow

Sampling allows Servers to request the Client (specifically, the Host application) to perform LLM interactions.

* Enables server-driven agentic behaviors and potentially **recursive or multi-step interactions**.
* Use cases: Complex multi-step tasks, autonomous agent workflows, interactive processes.

**Example:** A Server might request the Client to analyze data it has processed:

```python
def request_sampling(messages, system_prompt=None, include_context="none"):
    """Request LLM sampling from the client."""
    # In a real implementation, this would send a request to the client
    return {
        "role": "assistant",
        "content": "Analysis of the provided data..."
    }
```

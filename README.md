# The General Idea

I primarily use AI for gathering information and speeding up the process of using a search engine. I believe it's up to the user to actually investigate the provided material, as I've had an LLM tell me the wrong info way too many times.

I don't like paying for AI subscriptions either (well... who does?), since now I have enough technical knowledge to not need all the tokens that a paid plan provides.

**So, this is kind of what lead me to this project:** The goal is to create a local LLM with enough provided tools to act as a "research assistant" (even though I'm not a huge fan of that phrase). The intention is to have a model that runs well locally on a Macbook M4 chip (the base 16 GB model). It will be used strictly for gathering information together, give a general idea of the provided info, and provide links to the information it gathered.


To summarize, I'm trying to create an extremely scaled down version of [Perplexity](https://www.perplexity.ai/) that runs locally with low hardware requirements.

# The Models I'm Using

* [bartowski/Qwen2.5-7B-Instruct-Q4_K_M.gguf](https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/blob/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf)
* [Qwen/Qwen3-Embedding-8B-GGUF](https://huggingface.co/Qwen/Qwen3-Embedding-8B-GGUF?show_file_info=Qwen3-Embedding-8B-Q6_K.gguf)

# Post-Project Conclusions

This project (unsurprisingly) ended up with a lot more things to do than anticipated, many of which I'm going to cover in a new repository. Essentially, my initial idea of webscraping the internet and feeding those results into a model for it to use were successful.

However, there's a billion things that can be improved upon here, including:

## Web scraping refinement

Perfecting the web scraping was not a massive priority here, yet it could be greatly improved upon. As of now, I'm only grabbing HTML text matching the `p` (paragraph) tag. These results are then fed into the model to summarize them (as a temporary fix for webscraping) in preparation for embedding the model with the given information. Embedding the model is where I ran into some issues and has now been reassigned to a new project. This is where I'll create a full pipeline that involves scraping the data, creating a vector database for the relevant material, and embedding the model with said material.

The web search results as of now are unused for this reason, as feeding the raw text is not an option for me. This would defeat the purpose of an efficient system for local AI. So, I'm expanding on this project in [this repository](https://github.com/crdcamp/llama-cpp-llm-embedding).

## Embedding Pipeline

As I've already touched on, this project ended up leading into embedding the relevant info for the user's query. As a result, the project began expanding futher than its initial goal: Gathering website content and presenting it to a local model to ensure more accurate results. While the initial goal has been accomplished, embedding the model would be the next step.

## Final Concerns

This project has the potential to branch into a billion different hand-made capabilities for local models. From web scraping, to embedding, to RAG, to context management and a bunch of other things... I think there is still much to be done.

Regardless, the baseline requirements have been met. Moreover, the webscraping code is a strong foundation that will save me a lot of time implementing further improvements here. All in all, this project is considered concluded and will likely lead to several other repositories that build upon this idea.

For now, this `README.md` will serve as a template for how to approach this project.

# The General Idea

I primarily use AI for gathering information and speeding up the process of using a search engine. I believe it's up to the user to actually investigate the provided material, as I've had an LLM tell me the wrong info way too many times.

I don't like paying for AI subscriptions either, since now that I've gained enough understanding of coding to the point where I don't need all the tokens that a paid plan provides.

**So, this is kind of what lead me to this project:** The goal is to create a local LLM with enough provided tools to act as a "research assistant" (even though I'm not a huge fan of that phrase). The intention is to have a model that runs well locally on a Macbook M4 chip. It will be used strictly for gathering information together, give a general idea of the provided info, and (most importantly) provide links to the information it gathered.

# Project Structure

While I've touched on the relevant material for making something like this happen in the past, it wasn't until now that I've actually thought of a way to make this work and be legitimately useful. So, here's how we're gonna structure it:

## llama.cpp

[llama.cpp](https://github.com/ggml-org/llama.cpp) is the entry point for this project. It requires models to be stored in a [GGUF](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) file format, which enables fast loading and saving of models. Essentially, it's just a way to get these models running a bit more smoothly in the Python scripts, while avoiding the need to load a model each time a script is run (an issue I didn't know how to sidestep in the past).

[llama.cpp](https://github.com/ggml-org/llama.cpp) also has [`llama-cli`](https://github.com/ggml-org/llama.cpp?tab=readme-ov-file#llama-cli) which can be used for experimenting with these models. So, I won't have to make any sort of interface for testing or mess around with code too much once I get this set up.

Moreover, you can also [quantize models](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md), which reduces the precision of their weights which also requires less computational demand (I'm sure I'm leaving out many technical details here but that's the general idea). I can play around with this if needed, but I'm hoping I won't need to.

Finally, I believe (I'll have to confirm this later) that I can have this project run in a web page with a nice interface. But, that's a problem I'll have to get to and sort out later.

## The Process

1) Give input prompt (a research question)
1) Generate 5 internet searches to execute for input prompt
1) Use a tool to search the internet for each of these prompts
1) Gather the top 3 results of each of the 5 searches
1) Summarize the information with links provided for each.

This process is definitely gonna have some changes (and challenges) along the way, but this is the general idea we're going for. If the local LLMs can't generate good google searches, then we might have to look into training them with the Claude API. Before then, we'll just get this general workflow working and fine tune everything after the initial structure is ready.

# %% Imports
from llama_cpp import Llama

# llm = Llama.from_pretrained(
# 	repo_id="google/gemma-7b-it",
# 	filename="gemma-7b-it.gguf",
# )

# %% Figuring things out
llm.create_chat_completion(
	messages = [
		{
			"role": "user",
			"content": "What is the capital of France?"
		}
	]
)

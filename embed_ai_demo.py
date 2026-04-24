from llama_cpp import Llama

llm = Llama(
    model_path="./models/your-model.Q4_K_M.gguf",
    embedding=True,   # enable embedding mode
    n_ctx=512,
    n_gpu_layers=-1,  # offload all layers to GPU if available
)

embedding = llm.create_embedding("your text here")
vector = embedding["data"][0]["embedding"]

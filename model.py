from transformers import pipeline
import torch

model_id = "meta-llama/Llama-3.2-3B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",  # Forces CPU usage
    torch_dtype=torch.float16,  # float16 is more compatible across devices
)

prompt = "Explain the theory of relativity in simple terms."
response = pipe(prompt, max_new_tokens=256)
print(response[0]["generated_text"])



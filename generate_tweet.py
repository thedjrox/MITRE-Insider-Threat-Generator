import argparse
from transformers import pipeline
import torch

model_id = "meta-llama/Llama-3.2-3B-Instruct"

parser = argparse.ArgumentParser(description="Script to process threat types.")

parser.add_argument(
    "--threat_type",
    type=str,
    choices=["malicious", "medical", "normal"],
    required=True,
    help="Specify the type of threat: 'malicious', 'medical', or 'normal'."
)

args = parser.parse_args()

pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",  # Forces CPU usage
    torch_dtype=torch.float16,  # float16 is more compatible across devices
)

prompt = f"Write a tweet that impersonates a {args.threat_type} insider threat."
response = pipe(prompt, max_new_tokens=125)
print(response[0]["generated_text"])



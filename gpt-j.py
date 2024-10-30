import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Load the pre-trained model and tokenizer
model_name = "EleutherAI/gpt-neo-1.3B"  # or "EleutherAI/gpt-neo-2.7B"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name)

# Move the model to GPU if available
if torch.cuda.is_available():
    model = model.to("cuda")

# Define the prompt for text generation
prompt = "Generate a tweet that impersonates an insider threat:"

# Tokenize the input
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Create attention mask (1 for real tokens, 0 for padding)
attention_mask = torch.ones(input_ids.shape, device=input_ids.device)

# Move input and attention mask to GPU if available
if torch.cuda.is_available():
    input_ids = input_ids.to("cuda")
    attention_mask = attention_mask.to("cuda")

# Generate text
output = model.generate(
    input_ids,
    attention_mask=attention_mask,  # Pass the attention mask
    max_length=150,  # Maximum length of the generated text
    num_return_sequences=1,  # Number of generated sequences
    no_repeat_ngram_size=2,  # Avoid repeating n-grams
    early_stopping=True,  # Stop early if end of sentence is generated
    pad_token_id=tokenizer.eos_token_id  # Set pad token ID to eos token ID
)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)



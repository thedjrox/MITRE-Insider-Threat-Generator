from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer


def generate_response(model, tokenizer, message):
    prompt = str(message)

    inputs = tokenizer(prompt, return_tensors="pt")
    
    outputs = model.generate(inputs['input_ids'], max_length=200, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response
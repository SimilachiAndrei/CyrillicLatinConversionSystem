from transformers import T5ForConditionalGeneration, T5TokenizerFast

# Load the final model + tokenizer from disk
model = T5ForConditionalGeneration.from_pretrained("t5_translit_finetuned/checkpoint-1000")
tokenizer = T5TokenizerFast.from_pretrained("t5_translit_finetuned/checkpoint-1000")

# Example inference
def transliterate_text(text):
    inputs = tokenizer("transliterate: " + text, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=128)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print(transliterate_text("Пример текста"))  # → "Primer teksta"

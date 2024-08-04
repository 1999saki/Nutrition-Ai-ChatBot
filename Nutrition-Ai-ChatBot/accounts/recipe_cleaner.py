from os.path import dirname, abspath, join

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

BASE_DIR = dirname(dirname(abspath(__file__)))
CONTENT_DIR = join(BASE_DIR, 'content/trained_model')

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("flax-community/t5-recipe-generation")
model = AutoModelForSeq2SeqLM.from_pretrained(CONTENT_DIR)


def generate_recipe(input_ingredients):
    # Example ingredients
    input_ingredients = ", ".join(input_ingredients)

    # Tokenize the input
    inputs = tokenizer(input_ingredients, return_tensors="pt", padding="max_length",
                       truncation=True, max_length=512)

    # Generate the recipe
    with torch.no_grad():
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=150,  # Adjust max_length to control output size
            num_beams=2,  # Reduce number of beams for faster generation
            early_stopping=True,
            no_repeat_ngram_size=4,  # Prevent repetition
            temperature=0.7  # Control randomness, lower values make output more focused
        )

    # Decode the generated tokens
    generated_recipe = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_recipe


if __name__ == "__main__":
    generate_recipe()


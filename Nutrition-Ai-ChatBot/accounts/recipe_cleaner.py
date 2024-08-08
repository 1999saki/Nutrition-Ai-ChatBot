from os.path import join
from transformers import pipeline

# import spacy
import torch
from django.conf import settings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

CONTENT_DIR = join(settings.BASE_DIR, 'content/trained_model')

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("flax-community/t5-recipe-generation")


def generate_recipe(input_ingredients):
    model = AutoModelForSeq2SeqLM.from_pretrained(CONTENT_DIR)

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


# # Load the spaCy English model
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     # If the model is not found, download it and then load it
#     import spacy.cli
#
#     spacy.cli.download("en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")
#
# # Define a set of keywords related to generating recipes
# RECIPE_KEYWORDS = {'recipe', 'cook', 'prepare', 'make', 'generate', 'create'}


# def extract_food_items(text):
#     """
#     Check if the text is related to generating recipes and extract food items.
#
#     :param text: The input string to check and extract food items from.
#     :return: A tuple (bool, list) where the bool indicates if the text is related to recipes,
#              and the list contains extracted food items.
#     """
#     # Check if the text contains any recipe-related keywords
#     contains_recipe_keyword = any(
#         keyword in text.lower() for keyword in RECIPE_KEYWORDS)
#
#     if not contains_recipe_keyword:
#         return False, []
#
#     # Load the pre-trained NER pipeline from Hugging Face
#     ner_pipeline = pipeline("ner",
#                             model="dbmdz/bert-large-cased-finetuned-conll03-english",
#                             aggregation_strategy="simple")
#
#     # Use the pipeline to identify named entities
#     entities = ner_pipeline(text)
#
#     # Extract food items (considering "MISC" as a potential label for food items)
#     food_items_found = [entity['word'] for entity in entities if
#                         entity['entity_group'] in {"MISC"}]
#
#     return True, food_items_found


# Example usage
if __name__ == "__main__":
    test_string = "Can you generate a recipe with rice, chicken, and tomato?"
    # is_recipe_related, extracted_food_items = extract_food_items(test_string)
    # print("Is recipe related:", is_recipe_related)
    # print("Extracted food items:", extracted_food_items)

    print(generate_recipe(['rice', 'banana', 'chicken']))

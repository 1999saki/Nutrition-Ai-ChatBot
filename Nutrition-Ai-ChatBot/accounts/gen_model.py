# Load the fine-tuned model and tokenizer
from os.path import join

from django.conf import settings
from transformers import AutoTokenizer, AutoModelForCausalLM

CONTENT_DIR = join(settings.BASE_DIR, 'content/fine_tuned')

tokenizer = AutoTokenizer.from_pretrained(CONTENT_DIR)
model = AutoModelForCausalLM.from_pretrained(CONTENT_DIR)


# Function to generate a response
def generate_response(prompt, max_length=150, num_beams=5, early_stopping=True):

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        num_return_sequences=1,
        num_beams=num_beams,  # Beam search for better quality
        early_stopping=early_stopping,
        pad_token_id=tokenizer.eos_token_id  # Set pad token id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


if __name__ == "__main__":
    # Test the chatbot with some example questions
    example_questions = [
        "What is a healthy diet?"
    ]

    # Generate and print responses for the example questions
    for question in example_questions:
        print(f"Question: {question}")
        print(f"Response: {generate_response(question)}")
        print("-" * 50)

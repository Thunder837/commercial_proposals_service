from PIL import Image
import pytesseract
from transformers import pipeline

def process_image_with_ai(input_filepath, output_filepath):
    image = Image.open(input_filepath)
    extracted_text = pytesseract.image_to_string(image, lang="rus")

    ai_model = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    improved_text = ai_model(extracted_text, max_length=1024, truncation=True)[0]['generated_text']

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(improved_text)

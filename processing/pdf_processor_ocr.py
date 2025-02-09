import pytesseract
from pdf2image import convert_from_path
from transformers import pipeline

def extract_text_from_pdf(input_pdf):
    pages = convert_from_path(input_pdf, dpi=300)
    extracted_text = "\n".join([pytesseract.image_to_string(page, lang="rus") for page in pages])
    return extracted_text

def process_text_with_ai(text):
    ai_model = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    return ai_model(text, max_length=1024, truncation=True)[0]['generated_text']

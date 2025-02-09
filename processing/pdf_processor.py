import os
import re
from pdfminer.high_level import extract_text
from transformers import pipeline
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def process_text_with_ai(text):
    ai_model = pipeline("text2text-generation", model="facebook/bart-large-cnn")
    return ai_model(text, max_length=1024, truncation=True)[0]['generated_text']

def extract_text_from_pdf(input_filepath):
    return extract_text(input_filepath)

def create_pdf(text, output_filepath):
    c = canvas.Canvas(output_filepath, pagesize=A4)
    c.setFont("Helvetica", 12)
    y_position = 800

    for line in text.split("\n"):
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 800
        c.drawString(40, y_position, line)
        y_position -= 14

    c.save()

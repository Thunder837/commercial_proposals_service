import openai
import os
from docx import Document

openai.api_key = os.getenv("OPENAI_API_KEY")

def improve_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помощник, который улучшает текст коммерческих предложений."},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]

def process_word(input_filepath, output_filepath):
    doc = Document(input_filepath)

    for para in doc.paragraphs:
        para.text = improve_text(para.text)

    doc.save(output_filepath)

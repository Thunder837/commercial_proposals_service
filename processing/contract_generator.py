import os
import openai
from datetime import datetime
from docxtpl import DocxTemplate

# Установка API-ключа OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Определение формы собственности компании через GPT-4
def determine_company_type(company_name):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Ты помощник, который определяет юридическую форму компании."},
                  {"role": "user", "content": f"Определи форму собственности для компании: {company_name}"}]
    )
    return response["choices"][0]["message"]["content"]

def generate_contract(details, output_path):
    """Генерирует договор на основе шаблона и данных заказчика."""
    template_path = os.path.join("templates", "contracts", "contract_template.docx")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Шаблон {template_path} не найден!")

    # Определяем дату
    today = datetime.today()
    details["contract_number"] = today.strftime("%d-%m-%Y")  # 16-01-2025
    details["day"] = today.strftime("%d")
    details["month"] = today.strftime("%B").capitalize()  # Февраля
    details["year"] = today.strftime("%Y")

    # Определяем юр. лицо заказчика
    details["client_company_type"] = determine_company_type(details["client_company"])

    # Генерируем документ
    doc = DocxTemplate(template_path)
    doc.render(details)

    # Убедимся, что сохраняем в формате .docx
    if not output_path.endswith(".docx"):
        output_path += ".docx"

    doc.save(output_path)

    print(f"✅ Договор успешно создан: {output_path}")

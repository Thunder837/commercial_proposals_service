import os
import openai
import logging
import webbrowser
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from processing.word_processor import process_word
from processing.contract_generator import generate_contract
from database.database import save_client

# Пути к папкам
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "../output")
LOG_FOLDER = os.path.join(BASE_DIR, "../logs")

# Создаем папки, если они не существуют
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Настраиваем логирование
log_file = os.path.join(LOG_FOLDER, "errors.log")
logging.basicConfig(filename=log_file, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def log_error(message):
    logging.error(message)

# Настройки Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

# Устанавливаем API-ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload_kp', methods=['GET', 'POST'])
def upload_kp():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Нет файла в запросе", "danger")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == "":
            flash("Файл не выбран", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_filepath)

        output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], f"processed_{filename}")

        try:
            process_word(input_filepath, output_filepath)
        except Exception as e:
            log_error(f"Ошибка при обработке КП: {str(e)}")
            flash(f"Ошибка при обработке КП: {str(e)}", "danger")
            return redirect(request.url)

        return send_file(output_filepath, as_attachment=True)

    return render_template("upload_kp.html")

@app.route('/upload_contract', methods=['GET', 'POST'])
def upload_contract():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Нет файла в запросе", "danger")
            return redirect(request.url)

        file = request.files['file']
        filename = secure_filename(file.filename)
        input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_filepath)

        output_filename = f"contract_{datetime.now().strftime('%d-%m-%Y')}.docx"
        output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        try:
            contract_details = {
                "executor_company_key": request.form.get("executor_company_key", "ooo"),
                "client_company": request.form.get("client_company"),
                "client_company_type": request.form.get("client_company_type"),
                "client_legal_address": request.form.get("client_legal_address"),
                "client_actual_address": request.form.get("client_actual_address"),
                "client_inn": request.form.get("client_inn"),
                "client_kpp": request.form.get("client_kpp"),
                "client_ogrn": request.form.get("client_ogrn"),
                "client_bank_account": request.form.get("client_bank_account"),
                "client_bank_name": request.form.get("client_bank_name"),
                "client_bik": request.form.get("client_bik"),
                "client_corr_account": request.form.get("client_corr_account"),
                "client_email": request.form.get("client_email"),
                "client_phone": request.form.get("client_phone"),
                "client_director": request.form.get("client_director"),
            }

            generate_contract(contract_details, output_filepath)
            save_client(contract_details)

            if not os.path.exists(output_filepath):
                log_error("Ошибка: файл договора не был создан")
                flash("Ошибка: файл договора не был создан", "danger")
                return redirect(request.url)

        except Exception as e:
            log_error(f"Ошибка при создании договора: {str(e)}")
            flash(f"Ошибка при создании договора: {str(e)}", "danger")
            return redirect(request.url)

        return send_file(output_filepath, as_attachment=True, download_name=output_filename)

    return render_template("upload_contract.html")

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    webbrowser.open(url)  # Автоматически откроет браузер
    app.run(debug=True)

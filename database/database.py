import sqlite3

DB_FILE = "database/clients.db"

def init_db():
    """Создает таблицу заказчиков, если она не существует"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            legal_address TEXT,
            actual_address TEXT,
            inn TEXT,
            kpp TEXT,
            ogrn TEXT,
            bank_account TEXT,
            bank_name TEXT,
            bik TEXT,
            corr_account TEXT,
            email TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_client(details):
    """Сохраняет данные заказчика в БД"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (company_name, legal_address, actual_address, inn, kpp, ogrn, bank_account, 
                             bank_name, bik, corr_account, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        details.get("client_company", "Неизвестная компания"),
        details.get("client_legal_address", "Не указан"),
        details.get("client_actual_address", "Не указан"),
        details.get("client_inn", "Не указан"),
        details.get("client_kpp", "Не указан"),
        details.get("client_ogrn", "Не указан"),
        details.get("client_bank_account", "Не указан"),
        details.get("client_bank_name", "Не указан"),
        details.get("client_bik", "Не указан"),
        details.get("client_corr_account", "Не указан"),
        details.get("client_email", "Не указан"),
        details.get("client_phone", "Не указан")
    ))
    conn.commit()
    conn.close()

# Инициализация базы данных при запуске
init_db()

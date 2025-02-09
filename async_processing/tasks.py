from celery import Celery

# Настройка Celery с Redis
app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@app.task
def process_contract_async(details, output_filepath):
    """Фоновая обработка договора"""
    from processing.contract_generator import generate_contract
    generate_contract(details, output_filepath)
    return output_filepath

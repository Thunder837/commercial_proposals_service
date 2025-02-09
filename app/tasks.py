import logging

log_file = "logs/errors.log"
logging.basicConfig(filename=log_file, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def log_error(message):
    """Логирование ошибок"""
    logging.error(message)

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'test_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'client_encoding': 'UTF8'
}

# Список ID компаний для сбора данных (не менее 10)
EMPLOYER_IDS = [
    15478,  # Яндекс
    78638,  # VK
    1740,   # Сбер
    41926,  # Тинькофф
    3776,   # МТС
    9498,   # МегаФон
    2180,   # Билайн
    64174,  # Авито
    11224,  # X5 Group
    8455,   # Ozon
]
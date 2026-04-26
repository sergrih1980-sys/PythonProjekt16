import psycopg2
from src.api_client import HHApiClient
from config import DB_CONFIG


def validate_encoding():
    """Проверяет корректность кодировки параметров"""
    for key, value in DB_CONFIG.items():
        if isinstance(value, str):
            try:
                value.encode('utf-8')
            except UnicodeEncodeError:
                print(f"Проблема с кодировкой в параметре {key}: {value}")
                return False
    return True

@staticmethod
def create_database():
    if not validate_encoding():
        raise ValueError("Обнаружены некорректные символы в параметрах подключения")


class DBSetup:
    """Класс для создания и настройки БД"""

    @staticmethod
    def create_database():
        """Создаёт базу данных, если её нет"""
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']} WITH ENCODING 'UTF8'")
        except psycopg2.errors.DuplicateDatabase:
            pass  # БД уже существует
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_tables():
        """Создаёт таблицы в БД"""
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Таблица работодателей
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            hh_employer_id INTEGER UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL
        );
        """)

        # Таблица вакансий
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT,
            FOREIGN KEY (employer_id) REFERENCES employers(hh_employer_id)
        );
        """)

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def populate_data(employer_ids: list[int]):
        """Заполняет таблицы данными с hh.ru"""
        api_client = HHApiClient()
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        try:
            # Заполняем работодателей
            employers = api_client.get_employers(employer_ids)
            for employer in employers:
                cursor.execute(
                    "INSERT INTO employers (hh_employer_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (employer['id'], employer['name'])
                )

            # Заполняем вакансии
            for emp_id in employer_ids:
                vacancies = api_client.get_vacancies_by_employer(emp_id)
                for vacancy in vacancies:
                    salary = vacancy.get('salary', {})
                    cursor.execute(
                "INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url) VALUES (%s, %s, %s, %s, %s)",
                (
                    emp_id,
                    vacancy['name'],
            salary.get('from'),
            salary.get('to'),
            vacancy['alternate_url']
                )
            )

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
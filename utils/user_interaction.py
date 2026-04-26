from src.api_client import HHApiClient
from src.db_manager import DBManager
from src.db_setup import DBSetup
from typing import Optional

def user_interaction_flow():
    """
    Основная функция взаимодействия с пользователем.
    Использует экземпляры классов DBManager, HHApiClient и DBSetup без дублирования функциональности.
    Предоставляет понятный человекочитаемый интерфейс.
    """
    print("Добро пожаловать в систему анализа вакансий с hh.ru!\n")

    # Создаём экземпляры классов
    db_manager = DBManager()
    db_setup = DBSetup()
    api_client = HHApiClient()

    while True:
        print("=" * 50)
        print("Выберите действие:")
        print("1. Создать базу данных и таблицы")
        print("2. Загрузить данные с hh.ru")
        print("3. Показать компании и количество вакансий")
        print("4. Показать все вакансии")
        print("5. Показать среднюю зарплату")
        print("6. Показать вакансии с зарплатой выше средней")
        print("7. Поиск вакансий по ключевому слову")
        print("8. Выход")
        print("=" * 50)

        choice = input("\nВведите номер действия (1-8): ").strip()

        if choice == "1":
            _handle_create_database(db_setup)

        elif choice == "2":
            _handle_load_data(db_setup, api_client)

        elif choice == "3":
            _handle_companies_and_vacancies(db_manager)

        elif choice == "4":
            _handle_all_vacancies(db_manager)

        elif choice == "5":
            _handle_avg_salary(db_manager)

        elif choice == "6":
            _handle_higher_salary_vacancies(db_manager)

        elif choice == "7":
            _handle_keyword_search(db_manager)

        elif choice == "8":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 8.\n")



# Вспомогательные функции для обработки каждого действия

def _handle_create_database(db_setup):
    """Обрабатывает создание базы данных и таблиц"""
    try:
        db_setup.create_database()
        db_setup.create_tables()
        print("База данных и таблицы успешно созданы (если их не было).\n")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}\n")

def _handle_load_data(db_setup, api_client):
    """Обрабатывает загрузку данных с hh.ru"""
    try:
        # Пример ID работодателей (можно заменить на ввод от пользователя)
        employer_ids = [12345, 67890, 11223, 45678, 90123,
                     34567, 89012, 23456, 78901, 56789]

        print(f"Начинаем загрузку данных для {len(employer_ids)} компаний...")
        db_setup.populate_data(employer_ids)
        print(f"Данные успешно загружены для {len(employer_ids)} компаний.\n")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}\n")

def _handle_companies_and_vacancies(db_manager):
    """Показывает компании и количество вакансий"""
    try:
        data = db_manager.get_companies_and_vacancies_count()
        if not data:
            print("Нет данных о компаниях и вакансиях.\n")
            return

        print("\nСписок компаний и количество вакансий:")
        print("- " * 40)
        for company, count in data:
            print(f"{company}: {count} вакансий")
        print()
    except Exception as e:
        print(f"Ошибка при получении данных: {e}\n")

def _handle_all_vacancies(db_manager):
    """Показывает все вакансии"""
    try:
        data = db_manager.get_all_vacancies()
        if not data:
            print("Нет данных о вакансиях.\n")
            return

        print("\nВсе вакансии:")
        print("- " * 60)
        for company, title, salary_from, salary_to, url in data:
            salary_info = _format_salary(salary_from, salary_to)
            print(f"Компания: {company}")
            print(f"Вакансия: {title}")
            print(f"Зарплата: {salary_info}")
            print(f"Ссылка: {url}")
            print("- " * 60)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}\n")

def _handle_avg_salary(db_manager):
    """Показывает среднюю зарплату"""
    try:
        avg_salary = db_manager.get_avg_salary()
        print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f} руб.\n")
    except Exception as e:
        print(f"Ошибка при расчёте средней зарплаты: {e}\n")

def _handle_higher_salary_vacancies(db_manager):
    """Показывает вакансии с зарплатой выше средней"""
    try:
        data = db_manager.get_vacancies_with_higher_salary()
        if not data:
            print("Нет вакансий с зарплатой выше средней.\n")
            return

        print("\nВакансии с зарплатой выше средней:")
        print("- " * 60)
        for company, title, salary_from, salary_to, url in data:
            salary_info = _format_salary(salary_from, salary_to)
            print(f"Компания: {company}")
            print(f"Вакансия: {title}")
            print(f"Зарплата: {salary_info}")
            print(f"Ссылка: {url}")
            print("- " * 60)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}\n")

def _handle_keyword_search(db_manager):
    """Выполняет поиск вакансий по ключевому слову"""
    keyword = input("Введите ключевое слово для поиска: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым.\n")
        return

    try:
        data = db_manager.get_vacancies_with_keyword(keyword)
        if not data:
            print(f"По запросу '{keyword}' не найдено вакансий.\n")
            return

        print(f"\nРезультаты поиска по запросу '{keyword}':")
        print("- " * 60)
        for company, title, salary_from, salary_to, url in data:
            salary_info = _format_salary(salary_from, salary_to)
            print(f"Компания: {company}")
            print(f"Вакансия: {title}")
            print(f"Зарплата: {salary_info}")
            print(f"Ссылка: {url}")
            print("- " * 60)
    except Exception as e:
        print(f"Ошибка при поиске: {e}\n")

def _format_salary(salary_from: Optional[int], salary_to: Optional[int]) -> str:
    """Форматирует информацию о зарплате в человекочитаемый вид"""
    if salary_from is None and salary_to is None:
        return "не указана"
    elif salary_from is None:
        return f"до {salary_to} руб."
    elif salary_to is None:
        return f"от {salary_from} руб."
    else:
        return f"{salary_from} - {salary_to} руб."

# Запуск программы
if __name__ == "__main__":
    user_interaction_flow()
from db_setup import DBSetup
from config import EMPLOYER_IDS
from db_manager import DBManager

def main():
    # Создаём БД и таблицы
    DBSetup.create_database()
    DBSetup.create_tables()

    # Заполняем данными
    DBSetup.populate_data(EMPLOYER_IDS)

    # Создаём менеджер БД
    db_manager = DBManager()

    # Демонстрируем работу методов
    print("\n=== Компании и количество вакансий ===")
    companies_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, count in companies_vacancies:
        print(f"{company}: {count} вакансий")

    print("\n=== Средняя зарплата ===")
    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата: {avg_salary:.2f} руб.")

    print("\n=== Вакансии с зарплатой выше средней ===")
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for company, title, salary_from, salary_to, url in high_salary_vacancies[:5]:  # показываем первые 5
        print(f"{company} — {title}: {salary_from}-{salary_to} руб. — {url}")

    print("\n=== Вакансии по ключевому слову 'python' ===")
    python_vacancies = db_manager.get_vacancies_with_keyword('python')
    for company, title, salary_from, salary_to, url in python_vacancies[:5]:
        print(f"{company} — {title}: {salary_from}-{salary_to} руб. — {url}")

if __name__ == "__main__":
    main()
import psycopg2
from typing import List, Tuple, Optional
from config import DB_CONFIG


class DBManager:
    """Класс для работы с данными в БД PostgreSQL"""


    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        Returns:
            Список кортежей (название компании, количество вакансий).
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.hh_employer_id = v.employer_id
                GROUP BY e.name
                ORDER BY COUNT(v.vacancy_id) DESC;
            """)
            return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки.
        Returns:
            Список кортежей (компания, вакансия, зарплата от, зарплата до, ссылка).
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.hh_employer_id;
            """)
            return cursor.fetchall()

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям.
        Returns:
            Средняя зарплата (число).
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT AVG(
                    (COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2
                )
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
            """)
            result = cursor.fetchone()[0]
            return result if result is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список вакансий с зарплатой выше средней.
        Returns:
            Список кортежей (компания, вакансия, зарплата от, зарплата до, ссылка).
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.hh_employer_id
                WHERE (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 > %s;
            """, (avg_salary,))
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список вакансий, в названии которых содержатся переданные слова.
        Args:
            keyword: Ключевое слово для поиска.
        Returns:
            Список кортежей (компания, вакансия, зарплата от, зарплата до, ссылка).
        """
        search_pattern = f"%{keyword}%"
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.hh_employer_id
                WHERE LOWER(v.title) LIKE LOWER(%s);
            """, (search_pattern,))
            return cursor.fetchall()
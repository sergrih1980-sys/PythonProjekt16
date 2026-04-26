import requests
import time
from typing import List, Dict

class HHApiClient:
    """Класс для взаимодействия с API hh.ru"""

    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_employers(employer_ids: List[int]) -> List[Dict]:
        """
        Получает данные о работодателях по их ID.

        Args:
            employer_ids: Список ID работодателей.

        Returns:
            Список словарей с данными о работодателях.
        """
        employers = []
        for emp_id in employer_ids:
            response = requests.get(f"{HHApiClient.BASE_URL}/employers/{emp_id}")
            if response.status_code == 200:
                employers.append(response.json())
            time.sleep(0.1)  # Задержка для соблюдения лимитов API
        return employers

    @staticmethod
    def get_vacancies_by_employer(employer_id: int) -> List[Dict]:
        """
        Получает вакансии для конкретного работодателя.

        Args:
            employer_id: ID работодателя.

        Returns:
            Список словарей с данными о вакансиях.
        """
        vacancies = []
        page = 0
        per_page = 100

        while True:
            params = {
                'employer_id': employer_id,
                'page': page,
                'per_page': per_page
            }
            response = requests.get(
                f"{HHApiClient.BASE_URL}/vacancies",
                params=params
            )
            if response.status_code != 200:
                break

            data = response.json()
            vacancies.extend(data['items'])

            if page >= data['pages'] - 1:
                break
            page += 1
            time.sleep(0.1)

        return vacancies
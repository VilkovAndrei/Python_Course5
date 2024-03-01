import requests
import time


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    url_emp = "https://api.hh.ru/employers/"
    url_vac = "https://api.hh.ru/vacancies/"

    def __init__(self, emp_ids: list, area: int = 113):
        self.emp_ids = emp_ids

        self.params_vac = {
            "employer_id": emp_ids[0],
            "per_page": 20,
            "page": int,
            "only_with_salary": True,
            "area": area,
            "archived": False,
        }
        self.vacancies = []
        self.employers = []

    def get_request_emp(self, emp_id: str):
        response = requests.get(self.url_emp + emp_id)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения данных работодателя {emp_id}! Статус: {response.status_code}")
        return response.json()

    def get_employers(self):
        self.employers = []
        formatted_employers = []
        for emp_id in self.emp_ids:
            try:
                employer_data = self.get_request_emp(emp_id)
            except Exception as error:
                print(error)
            else:
                self.employers.append(employer_data)
            finally:
                time.sleep(0.5)

        for employer in self.employers:
            formatted_employer = {
                "employer_hh_id": employer['id'],
                "name": employer["name"],
                "url": employer["alternate_url"],
            }
            formatted_employers.append(formatted_employer)
        return formatted_employers

    def get_request_vac(self):
        response = requests.get(self.url_vac, params=self.params_vac)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()

    def get_vacancies(self, pages_count=5):
        count_vacancies = 0
        self.vacancies = []
        formatted_vacancies = []

        for employer in self.employers:
            employer_vacancies = []
            self.params_vac["employer_id"] = employer["id"]
            # print(f"employer_id={employer['id']}")
            for page in range(pages_count):
                page_vacancies = []
                self.params_vac["page"] = page
                # print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
                try:
                    page_vacancies = self.get_request_vac()
                except Exception as error:
                    print(error)
                else:
                    employer_vacancies.extend(page_vacancies["items"])
                    # print(f"Загружено вакансий: {len(page_vacancies)}")
                    count_vacancies += len(page_vacancies)
                finally:
                    time.sleep(0.5)
                if len(page_vacancies) == 0:
                    break
            self.vacancies.append(employer_vacancies)
            # print(f"({self.__class__.__name__}) Загружено вакансий всего: {count_vacancies}")

            for vacancy in employer_vacancies:
                formatted_vacancy = {
                    "employer": vacancy["employer"]["name"],
                    "employer_id": employer["id"],
                    "title": vacancy["name"],
                    "url": vacancy["url"],
                    "salary_from": vacancy["salary"]["from"] if vacancy["salary"]["from"] else None,
                    "salary_to": vacancy["salary"]["to"] if vacancy["salary"]["to"] else None,
                    "requirement": vacancy["snippet"]["requirement"],
                }
                formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

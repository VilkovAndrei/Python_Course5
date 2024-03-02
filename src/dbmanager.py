import psycopg2


class DBManager:
    """Класс для работы с базой данных PostgreSQL."""

    def __init__(self, params: dict, db_name):
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()
        self.db_name = db_name
        self.params = params
        self.create_database(self.db_name)

    def create_database(self, database_name: str):
        """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

        self.conn.autocommit = True

        self.cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        self.cur.execute(f"CREATE DATABASE {database_name}")

        self.conn.close()
        self.params['dbname'] = self.db_name

        self.conn = psycopg2.connect(**self.params)

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    hh_id VARCHAR(10) NOT NULL
                )
            """)

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    title VARCHAR NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url VARCHAR(100)
                )
            """)

        self.conn.commit()
        print(f"\nБД {database_name} успешно создана")

    def insert_data(self, emp_data: list[dict], vac_data: list[dict]):
        """Заполнение таблиц данными."""

        with self.conn.cursor() as cur:
            for emp in emp_data:
                cur.execute(
                    f"INSERT INTO employers (name, hh_id) VALUES (%s, %s) RETURNING employer_id",
                    (emp["name"], emp["employer_hh_id"])
                )
                employer_id = cur.fetchone()[0]
                # print(f'employer_id = {employer_id}')
                for vac in vac_data:
                    if vac['employer_id'] == emp["employer_hh_id"]:
                        cur.execute(
                            f"INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url) VALUES (%s, %s, %s, %s, %s)",
                            (employer_id, vac["title"], vac["salary_from"], vac["salary_to"], vac["url"])
                        )

        self.conn.commit()
        print(f"\nБД {self.db_name} успешно заполнена")

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Получает из базы данных список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.name, COUNT(*) AS count_vacancies FROM vacancies
                    JOIN employers USING(employer_id) GROUP BY employers.name
                """
            )
            data = cur.fetchall()
            data_dict = [{"company": d[0], "count_vacancies": d[1]} for d in data]

        return data_dict

    def get_all_vacancies(self) -> list[dict]:
        """Получает из базы данных список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.name, title, salary_from, url  FROM vacancies
                    JOIN employers  USING(employer_id)
                """
            )
            data = cur.fetchall()
            data_dict = [{"company": d[0], "title": d[1], "salary_from": d[2], "url": d[3]} for d in data]

        return data_dict

    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary_from) FROM vacancies
                """
            )
            avg_salary = int(cur.fetchone()[0])

        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.name, title, salary_from, url  FROM vacancies
                    JOIN employers  USING(employer_id)
                    WHERE salary_from > ANY(SELECT AVG(salary_from) FROM vacancies)
                    ORDER BY salary_from DESC
                """
            )
            data = cur.fetchall()
            data_dict = [{"company": d[0], "title": d[1], "salary_from": d[2], "url": d[3]} for d in data]

        return data_dict

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT employers.name, title, salary_from, url  FROM vacancies JOIN employers  USING(employer_id) WHERE title LIKE '%{keyword}%'"
            )
            data = cur.fetchall()
            data_dict = [{"company": d[0], "title": d[1], "salary_from": d[2], "url": d[3]} for d in data]

        return data_dict

import psycopg2


class DBManager:
    """Класс для работы с базой данных PostgreSQL."""

    def __init__(self, params: dict):
        # self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        # self.cur = self.conn.cursor()
        self.db_name = 'hh_db'
        self.params = params
        self.create_database(self.db_name, self.params)

    def create_database(self, database_name: str, params: dict):
        """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    hh_id VARCHAR(10) NOT NULL
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    title VARCHAR NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url VARCHAR(100),
                    requirement TEXT
                )
            """)

        conn.commit()
        conn.close()

    def insert_data(self, emp_data: list[dict], vac_data: list[dict], params: dict):
        """Заполнение таблиц данными."""
        conn = psycopg2.connect(dbname=self.db_name, **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for emp in emp_data:
                cur.execute(
                    f"INSERT INTO employers (name, hh_id) VALUES (%s, %s) RETURNING employer_id",
                    (emp["name"], emp["employer_hh_id"])
                )
                employer_id = cur.fetchone()[0]
                for vac in vac_data:
                    if vac['employer_id'] == emp["employer_hh_id"]:
                        cur.execute(
                            f"INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url, requirement) VALUES (%s, %s, %s, %s, %s, %s)",
                            (employer_id, vac["title"], vac["salary_from"], vac["salary_to"], vac["url"], vac["requirement"])
                        )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает из базы данных список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """Получает из базы данных список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям, у которых указана зарплата."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self, keywords: tuple):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        pass

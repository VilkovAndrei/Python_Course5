import psycopg2


class DBManager:
    """Класс для работы с базой данных PosgreSQL."""

    def __init__(self, params: dict):
        # self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        # self.cur = self.conn.cursor()
        self.params = params
        self.create_database('hh_db', self.params)

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


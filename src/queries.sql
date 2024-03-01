""" Создание таблицы работодателей employers"""
CREATE TABLE employers (
    employer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hh_id VARCHAR(10) NOT NULL
)

""" Создание таблицы вакансий vacancies"""
CREATE TABLE vacancies (
    vacancy_id SERIAL PRIMARY KEY,
    employer_id INT REFERENCES employers(employer_id),
    title VARCHAR NOT NULL,
    salary_from INT,
    salary_to INT,
    url VARCHAR(100),
    requirement TEXT
)

"""Заполнение данными таблицы работодателей employers"""
f"INSERT INTO employers (name, employer_hh_id, url) VALUES (%s, %s, %s) RETURNING employer_id",
    (emp["name"], emp["employer_hh_id"], emp["url"])

"""Заполнение данными таблицы таблицы вакансий vacancies"""
f"INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url, requirement) VALUES (%s, %s, %s, %s, %s, %s)",
    (employer_id, vac["title"], vac["salary_from"], vac["salary_to"], vac["url"], vac["requirement"])


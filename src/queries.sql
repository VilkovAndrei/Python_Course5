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
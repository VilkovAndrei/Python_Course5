import psycopg2
from src.config import config
from src.headhunterapi import HeadHunterAPI
from src.dbmanager import DBManager


def main():
    """Список выбранных работодателей"""
    list_employers_id = [
        '64174',
        '78638',
        '2748',
        '3127',
        '1740',
        '93051',
        '4219',
        '907345',
        '1471727',
        '1057047'
    ]

    """Получаем данные от api.hh.ru"""

    print("Получаем данные от api.hh.ru. Подождите, пожалуйста!")
    hh = HeadHunterAPI(list_employers_id)
    emp_data = hh.get_employers()
    vac_data = hh.get_vacancies()

    """Работаем с БД PostgreSQL"""

    params_db = config()
    print("\nРаботаем с БД PostgreSQL")
    new_db_name = input("\nВведите название создаваемой БД:\n")
    # new_db_name = 'hh_db'
    try:
        db = DBManager(params_db, new_db_name)
        db.insert_data(emp_data, vac_data)

        data_dict = db.get_companies_and_vacancies_count()
        print(f"\nСписок компаний и количества вакансий:")
        print(data_dict)

        data_dict = db.get_all_vacancies()
        print("\nСписок вакансий:")
        print(data_dict)

        avg_salary = db.get_avg_salary()
        print(f"\nСредняя зарплата: {avg_salary}")

        data_dict = db.get_vacancies_with_higher_salary()
        print("\nСписок вакансий с зарплатой выше средней:")
        print(data_dict)

        keyword = input("\nВведите ключевое слово для поиска по вакансиям:\n")

        data_dict = db.get_vacancies_with_keyword(keyword)
        print(f"\nСписок вакансий, отфильтрованных по слову {keyword}:")
        print(data_dict)

        db.conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    main()

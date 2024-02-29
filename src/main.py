
from src.config import config
from src.headhunterapi import HeadHunterAPI
from src.dbmanager import DBManager


def main():
    list_employers_id = [
        # '3529',
        # '78638',
        # '2748',
        # '3127',
        # '1740',
        '93051',
        # '4219',
        # '907345',
        # '1471727',
        '1057047'
    ]

    hh = HeadHunterAPI(list_employers_id)
    emp_data = hh.get_employers()
    # print(emp_data_list)
    vac_data = hh.get_vacancies()
    # print(vac_data)

    params_db = config()
    db = DBManager(params_db)
    db.insert_data(emp_data, vac_data)


if __name__ == '__main__':
    main()

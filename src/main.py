
from src.config import config
from src.headhunterapi import HeadHunterAPI

def main():
    list_employers_id = list(
        3529,
        78638,
        2748,
        3127,
        1740,
        93051,
        4219,
        907345,
        1471727,
        1057047
    )
    params_db = config()
    hh = HeadHunterAPI(list_employers_id)



if __name__ == '__main__':
    main()



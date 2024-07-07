from src.parse_habr import get_habr_vacancies
from src.parse_avito import get_avito_vacancies
from src.database import clear_data


def main_func():
    pass


def load_habr():
    n = 0
    page = 1

    while True:
        vacancies, n = get_habr_vacancies(page, n)
        if not vacancies:
            break
        page += 1


def clear_bd():
    clear_data()

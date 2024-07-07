import requests
from bs4 import BeautifulSoup
from .database import insert_data


def get_habr_vacancies(page, count):
    url = f"https://career.habr.com/vacancies?page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36 "
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    vacancies = []

    for vacancy in soup.find_all('div', class_='vacancy-card'):
        title = vacancy.find('div', class_='vacancy-card__title').text.strip()
        company = vacancy.find('div', class_='vacancy-card__company-title').text.strip()
        link = "https://career.habr.com" + vacancy.find('a', class_='vacancy-card__icon-link')['href']

        salary = vacancy.find('div', class_='basic-salary').text.strip() \
            if vacancy.find('div', class_='basic-salary') else 'N/A'
        location = vacancy.find('div', class_='location').text.strip() if vacancy.find('div',
                                                                                       class_='location') else 'N/A'
        date_posted = vacancy.find('div', class_='vacancy-card__date').text.strip() \
            if vacancy.find('div', class_='vacancy-card__date') else 'N/A'
        work_schedule = vacancy.find('div', class_='vacancy-card__meta').text.strip() \
            if vacancy.find('div',class_='vacancy-card__meta') else 'N/A'
        remote_work = 'Удаленная работа' if 'Можно удаленно' in work_schedule else 'Офис'

        insert_data(count, title, company, salary, work_schedule, "HABR", link)
        count += 1

        vacancies.append({
            'title': title,
            'company': company,
            'link': link,
            'salary': salary,
            'location': location,
            'date_posted': date_posted,
            'work_schedule': work_schedule,
            'remote_work': remote_work
        })

    return vacancies, count

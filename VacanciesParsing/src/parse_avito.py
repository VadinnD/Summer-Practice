import requests
from bs4 import BeautifulSoup
import sqlite3


def get_avito_vacancies(page):
    url = f"https://www.avito.ru/moskva/rezume?p={page}"
    print(page)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    vacancies = []

    for vacancy in soup.find_all('div', class_='iva-item-content'):
        title = vacancy.find('h3', class_='title-root').text.strip()
        company = vacancy.find('div', class_='geo-georeferences').text.strip() if vacancy.find('div',
                                                                                               class_='geo-georeferences') else 'N/A'
        description = vacancy.find('div', class_='iva-item-text').text.strip() if vacancy.find('div',
                                                                                               class_='iva-item-text') else 'N/A'
        link = "https://www.avito.ru" + vacancy.find('a', class_='link-link-MbQDP')['href']

        salary = vacancy.find('span', class_='price-text').text.strip() if vacancy.find('span',
                                                                                        class_='price-text') else 'N/A'
        location = vacancy.find('div', class_='geo-georeferences').text.strip() if vacancy.find('div',
                                                                                                class_='geo-georeferences') else 'N/A'
        date_posted = vacancy.find('div', class_='date-root').text.strip() if vacancy.find('div',
                                                                                           class_='date-root') else 'N/A'

        # Placeholder values for work_schedule and remote_work
        work_schedule = 'N/A'
        remote_work = 'N/A'

        vacancies.append({
            'title': title,
            'company': company,
            'description': description,
            'link': link,
            'salary': salary,
            'location': location,
            'date_posted': date_posted,
            'work_schedule': work_schedule,
            'remote_work': remote_work
        })

    # print(vacancies)
    return vacancies

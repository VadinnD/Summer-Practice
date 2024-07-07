import os
import telebot
from telebot import types
from src.database import get_data, clear_data
from src.controller import load_habr

# TOKEN = os.getenv('TELEGRAM_TOKEN')
TOKEN = '7428234350:AAEFItZHXZW-k0xw4kLV9zREqfExar_K8PQ'
bot = telebot.TeleBot(TOKEN)

keyboard0 = types.ReplyKeyboardMarkup()
hh = True
habr = True
avito = True
user_state = {}
# vacancies = ''
company = ''
job = ''
flag = True
counts = 1


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Avito", "Habr", "HH", "Others")
    bot.send_message(message.chat.id, 'Привет! Выбери платформу для поиска работы:', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def helps(message):
    keyboard = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, 'Я умею: \n\n - Выводить по 10 вакансий \n'
                                      ' - Выводить вакансии с применением фильтров \n - и т.д.', reply_markup=keyboard)


# Обработка нажатия кнопки для выбора платформы
@bot.message_handler(func=lambda message: message.text in ["Avito", "Habr", "HH"])
def handle_platform_selection(message):
    global habr, avito, hh
    platform = message.text
    if platform == "Avito":
        if avito:
            pass
            # load avito
        bot.send_message(message.chat.id, 'В процессе разработки...', reply_markup=keyboard0)
    elif platform == "Habr":
        if habr:
            bot.send_message(message.chat.id, 'Загрузка данных, это займет некоторое время...')
            load_habr()
            habr = False
        bot.send_message(message.chat.id, f"Данные загружены с {platform}. Выберите действие:",
                         reply_markup=actions_keyboard())
    elif platform == "HH":
        if hh:
            pass
            # load hh
        bot.send_message(message.chat.id, 'В процессе разработки...', reply_markup=keyboard0)
    else:
        return

    # bot.send_message(message.chat.id, f"Данные загружены с {platform}. Выберите действие:",
    #                  reply_markup=actions_keyboard())


# Кнопки действий
def actions_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row("Показать любые 10 вакансий")
    keyboard.row("Показать вакансии в компании...")
    keyboard.row("Показать вакансии по специальности...")
    keyboard.row("Назад")
    return keyboard


@bot.message_handler(func=lambda message: message.text in ["Показать любые 10 вакансий",
                                                           "Показать вакансии в компании...",
                                                           "Показать вакансии по специальности...", "Назад"])
def handle_actions(message):
    if message.text == "Показать любые 10 вакансий":
        show_10_vacancies(message, 0)
    elif message.text == "Показать вакансии в компании...":
        msg = bot.send_message(message.chat.id, "Введите название компании:")
        user_state[message.chat.id] = 'waiting_for_company'
        bot.register_next_step_handler(msg, show_vacancies_by_company)
        # show_vacancies_by_company(msg, 0)
    elif message.text == "Показать вакансии по специальности...":
        msg = bot.send_message(message.chat.id, "Введите название вакансии:")
        user_state[message.chat.id] = 'waiting_for_company'
        bot.register_next_step_handler(msg, show_vacancies_by_title)
    elif message.text == "Назад":
        start(message)


def next_page_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row("Следующие 10 вакансий")
    keyboard.row("Нaзaд")
    return keyboard


def next_page_keyboard1():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row("Слeдующие 10 вакансий")
    keyboard.row("Нaзaд")
    return keyboard


def next_page_keyboard2():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row("Слeдующие 10 вaкансий")
    keyboard.row("Нaзaд")
    return keyboard


@bot.message_handler(func=lambda message: message.text in ["Следующие 10 вакансий", "Слeдующие 10 вакансий",
                                                           "Слeдующие 10 вaкансий", "Нaзaд"])
def next_page(message):
    global counts, flag
    if message.text == "Следующие 10 вакансий":
        show_10_vacancies(message, counts * 10)
        counts += 1
    elif message.text == "Слeдующие 10 вакансий":
        show_vacancies_by_company(message, counts * 10)
        counts += 1
    elif message.text == "Слeдующие 10 вaкансий":
        show_vacancies_by_title(message, counts * 10)
        counts += 1
        '''
        if user_state.get(message.chat.id) == 'showing_10_vacancies':
            print(1)
            #vacancy_offsets[message.chat.id] += 10
            #show_vacancies(message,
             #              f'SELECT * FROM public.jobs WHERE platform = \'HABR\' LIMIT 10 OFFSET {vacancy_offsets[message.chat.id]}',
              #             "всех вакансий")
        elif user_state.get(message.chat.id) == 'waiting_for_company':
            print(2)
            # show_next_vacancies_by_company(message)
        elif user_state.get(message.chat.id) == 'waiting_for_title':
            print(3)
            # show_next_vacancies_by_title(message)
        '''
    elif message.text == "Нaзaд":
        flag = True
        bot.send_message(message.chat.id, f"Выберите действие:",
                         reply_markup=actions_keyboard())


def show_10_vacancies(message, i):
    vacancies = get_data('SELECT * FROM public.jobs WHERE platform = \'HABR\';')

    if i >= len(vacancies):
        return

    response = f'Найдено вакансий: {len(vacancies)}   \nСтраница: {i // 10 + 1}/{len(vacancies) // 10 + 1}\n\n'

    for vacancy in range(i, len(vacancies)):
        response += (f'Должность: {vacancies[vacancy][1]}\n'
                     f'Компания: {vacancies[vacancy][2]}\n'
                     f'Зарплата: {vacancies[vacancy][3]}\n'
                     f'Описание: {vacancies[vacancy][4]}\n'
                     f'Ссылка: {vacancies[vacancy][6]}\n'
                     '--------------------------------------\n')
        i += 1
        if i % 10 == 0:
            break

    bot.send_message(message.chat.id, response, reply_markup=next_page_keyboard())


def show_vacancies_by_company(message, i=0):
    global company, flag
    if flag:
        company = message.text.strip()
        flag = False
    vacancies = get_data(f'SELECT * FROM public.jobs WHERE company = \'{company}\' AND platform = \'HABR\';')

    if i >= len(vacancies):
        return

    # company = message.text.lower().strip()

    # response = f'Найдено вакансий: {len(vacancies)}\n\n'
    response = f'Найдено вакансий: {len(vacancies)}   \nСтраница: {i // 10 + 1}/{len(vacancies) // 10 + 1}\n\n'

    for vacancy in range(i, len(vacancies)):
        response += (f'Должность: {vacancies[vacancy][1]}\n'
                     f'Компания: {vacancies[vacancy][2]}\n'
                     f'Зарплата: {vacancies[vacancy][3]}\n'
                     f'Описание: {vacancies[vacancy][4]}\n'
                     f'Ссылка: {vacancies[vacancy][6]}\n'
                     '--------------------------------------\n')
        i += 1
        if i % 10 == 0:
            break

    bot.send_message(message.chat.id, response, reply_markup=next_page_keyboard1())


def show_vacancies_by_title(message, i=0):
    global job, flag
    if flag:
        job = message.text.strip()
        flag = False
    vacancies = get_data(f'SELECT * FROM public.jobs WHERE job = \'{job}\' AND platform = \'HABR\';')

    if i >= len(vacancies):
        return

    # if user_state.get(message.chat.id) != 'waiting_for_company':
    #     return

    # job = message.text.lower().strip()
    # job = message.text.strip()

    # vacancies = get_data(f'SELECT * FROM public.jobs WHERE job = \'{job}\' AND platform = \'HABR\';')

    response = f'Найдено вакансий: {len(vacancies)}   \nСтраница: {i // 10 + 1}/{len(vacancies) // 10 + 1}\n\n'

    for vacancy in range(i, len(vacancies)):
        response += (f'Должность: {vacancies[vacancy][1]}\n'
                     f'Компания: {vacancies[vacancy][2]}\n'
                     f'Зарплата: {vacancies[vacancy][3]}\n'
                     f'Описание: {vacancies[vacancy][4]}\n'
                     f'Ссылка: {vacancies[vacancy][6]}\n'
                     '--------------------------------------\n')
        i += 1
        if i % 10 == 0:
            break

    bot.send_message(message.chat.id, response, reply_markup=next_page_keyboard2())


# @bot.message_handler(func=lambda message: message.text in ["Update"])
@bot.message_handler(commands=['update'])
def update(message):
    clear_data()
    start(message)


# Запуск бота
bot.polling()

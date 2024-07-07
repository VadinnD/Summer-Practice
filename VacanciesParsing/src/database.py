import psycopg2
import os
from .config import DATABASE


# DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(
        dbname=DATABASE['dbname'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        port=DATABASE['port']
    )

    # conn = psycopg2.connect(DATABASE_URL)
    return conn


def insert_data(number, title, company, salary, condition, type, link):
    conn = get_db_connection()
    cursor = conn.cursor()

    if type == "HABR":
        sql_query = f"""INSERT INTO public.jobs
                    VALUES
                    ({number}, '{title}', '{company}', '{salary}', '{condition}', '{type}', '{link}');"""
        try:
            cursor.execute(sql_query)
        except Exception as e:
            print(e)

    conn.commit()
    cursor.close()
    conn.close()


def clear_data():
    sql_query = "DELETE FROM jobs;"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()


def get_data(sql_query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    vacancies = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return vacancies


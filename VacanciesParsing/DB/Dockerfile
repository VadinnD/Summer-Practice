# Используем базовый образ PostgreSQL
FROM postgres:latest

# Устанавливаем переменные окружения для PostgreSQL
ENV POSTGRES_DB=VacanciesParser
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=root904

# Копируем дамп базы данных в контейнер
COPY backup.dump /docker-entrypoint-initdb.d/

EXPOSE 5432


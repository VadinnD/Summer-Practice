# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7070

# Команда для запуска бота
CMD ["python", "bot.py"]

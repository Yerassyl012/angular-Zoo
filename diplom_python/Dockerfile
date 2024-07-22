# Используйте официальный образ Python как родительский образ
FROM python:3.8-slim

# Установите рабочий каталог в контейнере
WORKDIR /app

# Копируйте файлы зависимостей в текущую директорию
COPY requirements.txt requirements.txt

# Установите любые необходимые пакеты, указанные в requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте содержимое локального каталога src в рабочий каталог
COPY . .

# Сделайте порт доступным для мира за пределами этого контейнера
EXPOSE 5000

# Определите переменные среды
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Запустите приложение при запуске контейнера
CMD ["flask", "run"]

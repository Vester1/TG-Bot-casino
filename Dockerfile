FROM python:3.12-alpine

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]

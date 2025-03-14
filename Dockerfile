FROM python:3.9-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY main.py /app/
COPY src/ /app/src/

# Создаем директорию для данных
RUN mkdir -p /app/data

# Запускаем приложение
CMD ["python3", "/app/main.py"]
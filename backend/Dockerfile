FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt из корня контекста (./backend) в /app/backend/
COPY requirements.txt /app/backend/
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

# Копируем все файлы из корня контекста (./backend) в /app/backend/
COPY . /app/backend/

# Добавляем /app в PYTHONPATH, чтобы backend был модулем
ENV PYTHONPATH=/app

# Запускаем Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
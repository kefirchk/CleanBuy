FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--loop", "asyncio", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "certs/key.pem", "--ssl-certfile", "certs/cert.pem"]

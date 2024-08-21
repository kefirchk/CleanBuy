FROM python:3.11-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["alembic", "upgrade", "head"]
CMD ["sh", "-c", "sleep 5 && uvicorn src.main:app --host 0.0.0.0 --port 443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem"]

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./data ./data    # 👈 سيتم نسخ data من مجلد backend (بعد نقله)

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

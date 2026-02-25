FROM python:3.10-slim

WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ مجلد backend بالكامل
COPY ./app ./app

# نسخ مجلد data من خارج مجلد backend
COPY ../data ./data

# تحديد المتغيرات البيئية
ENV PYTHONPATH=/app
ENV DATA_PATH=/app/data

# تشغيل التطبيق
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

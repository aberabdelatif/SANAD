FROM python:3.10-slim

# المجلد الأساسي داخل الحاوية
WORKDIR /app

# نسخ dependencies
COPY ../requirements.txt .   
RUN pip install --no-cache-dir -r requirements.txt

# نسخ مجلد التطبيق والبيانات
COPY ./app ./app
COPY ./data ./data

# نقطة البداية
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

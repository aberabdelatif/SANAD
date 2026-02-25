import os
from pathlib import Path

print("🔍 ===== بدء التشخيص ===== ")
print(f"📁 المجلد الحالي: {os.getcwd()}")
print("📁 محتويات المجلد الرئيسي:")
try:
    for item in os.listdir('.'):
        print(f"   - {item}")
except Exception as e:
    print(f"   خطأ: {e}")

print("\n📁 محتويات مجلد /app (إذا كان موجوداً):")
try:
    for item in os.listdir('/app'):
        print(f"   - {item}")
except:
    print("   لا يمكن قراءة /app")

print("\n📁 البحث عن مجلد البيانات:")
possible_paths = [
    '/app/data',
    '/app/données',
    '/app/backend/data',
    '/data',
    './data',
    './données'
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"✅ موجود: {path}")
        if os.path.isdir(path):
            try:
                contents = os.listdir(path)[:5]  # أول 5 عناصر فقط
                print(f"   المحتويات: {contents}")
            except:
                print(f"   لا يمكن قراءة المحتويات")
    else:
        print(f"❌ غير موجود: {path}")

print("🔍 ===== نهاية التشخيص ===== \n")

# باقي الكود بعد ذلك...
from fastapi import FastAPI
# ... rest of your code

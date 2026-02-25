import os
from pathlib import Path

print("🔍 ===== تشخيص المسارات ===== ")
print(f"📁 الموقع الحالي: {os.getcwd()}")
print("📁 محتويات /app:")
try:
    for item in os.listdir('/app'):
        print(f"   - {item}")
except:
    print("   لا يمكن القراءة")

print("\n📁 محتويات /app/data (إذا موجود):")
if os.path.exists('/app/data'):
    try:
        for item in os.listdir('/app/data'):
            print(f"   - {item}")
    except:
        print("   خطأ في القراءة")
else:
    print("   ❌ مجلد data غير موجود في /app/data")

print("🔍 ===== نهاية التشخيص ===== \n")

# باقي الكود...
from fastapi import FastAPI
# ...

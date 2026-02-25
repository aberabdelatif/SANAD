import os
from pathlib import Path

print("🔍 تشخيص المجلدات:")
print(f"المجلد الحالي: {os.getcwd()}")
print("محتويات مجلد /app:")
try:
    for item in os.listdir('/app'):
        print(f"  - {item}")
except:
    print("  لا يمكن قراءة المجلد")

print("\nمحتويات مجلد /app/données (إذا موجود):")
try:
    if os.path.exists('/app/données'):
        for item in os.listdir('/app/données'):
            print(f"  - {item}")
    else:
        print("  مجلد données غير موجود!")
except Exception as e:
    print(f"  خطأ: {e}")

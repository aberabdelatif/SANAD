# هذا الملف مخصص للتوافق مع MongoDB مستقبلاً
# حالياً نستخدم JSON مباشرة

from .config import DATA_PATH
import os
import json

def check_data_available():
    """التحقق من وجود بيانات JSON"""
    if DATA_PATH and os.path.exists(DATA_PATH):
        return True
    return False

def get_data_path():
    """إرجاع مسار البيانات"""
    return DATA_PATH 

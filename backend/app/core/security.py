from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from typing import Optional
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta

# إعدادات الأمان
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
API_KEYS = {
    "test_key_123": {"user": "test_user", "role": "user"},
    "admin_key_456": {"user": "admin", "role": "admin"}
}

# معدل الطلبات (Rate Limiting)
RATE_LIMIT = {}
MAX_REQUESTS_PER_MINUTE = 60

class SecurityService:
    """خدمة الأمان والمصادقة"""
    
    @staticmethod
    async def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> dict:
        """
        التحقق من صحة مفتاح API
        """
        if not api_key:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="مطلوب مفتاح API"
            )
        
        user_info = API_KEYS.get(api_key)
        if not user_info:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="مفتاح API غير صالح"
            )
        
        # التحقق من معدل الطلبات
        SecurityService.check_rate_limit(api_key)
        
        return user_info
    
    @staticmethod
    def check_rate_limit(api_key: str):
        """
        التحقق من معدل الطلبات
        """
        now = datetime.now()
        minute_key = now.strftime("%Y-%m-%d-%H-%M")
        key = f"{api_key}:{minute_key}"
        
        # تحديث العداد
        if key in RATE_LIMIT:
            RATE_LIMIT[key] += 1
        else:
            RATE_LIMIT[key] = 1
        
        # التحقق من الحد الأقصى
        if RATE_LIMIT[key] > MAX_REQUESTS_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail="تجاوزت حد الطلبات المسموح. حاول بعد دقيقة"
            )
    
    @staticmethod
    def hash_text(text: str) -> str:
        """
        تشفير نص باستخدام SHA256
        """
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def create_signature(data: dict, secret: str) -> str:
        """
        إنشاء توقيع للبيانات
        """
        message = json.dumps(data, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    @staticmethod
    def verify_signature(data: dict, signature: str, secret: str) -> bool:
        """
        التحقق من صحة التوقيع
        """
        expected = SecurityService.create_signature(data, secret)
        return hmac.compare_digest(expected, signature)

# دوال مساعدة للمسارات
async def get_current_user(api_key: str = Security(API_KEY_HEADER)):
    """
    الحصول على المستخدم الحالي (للاستخدام في المسارات المحمية)
    """
    user_info = await SecurityService.verify_api_key(api_key)
    return user_info

async def require_admin(api_key: str = Security(API_KEY_HEADER)):
    """
    التحقق من أن المستخدم Admin
    """
    user_info = await SecurityService.verify_api_key(api_key)
    if user_info.get("role") != "admin":
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="هذه الميزة متاحة فقط للمشرفين"
        )
    return user_info

# مثال للاستخدام في main.py
"""
from .core.security import get_current_user, require_admin

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"مرحباً {user['user']}"}

@app.get("/admin-only")
async def admin_route(user: dict = Depends(require_admin)):
    return {"message": "مرحباً أيها المشرف"}
"""

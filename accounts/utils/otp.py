import random
from django.conf import settings
from django.core.cache import cache


def generate_otp_code() -> str:
    """
    Generate a 4-digit OTP code.
    """
    return str(random.randint(1000, 9999))


def get_otp_cache_key(phone: str) -> str:
    """
    Construct cache key for storing OTP by phone.
    """
    return f"otp:{phone}"


def set_otp_code(phone: str, code: str) -> None:
    """
    Store OTP code in Redis with expiration.
    """
    key = get_otp_cache_key(phone)
    cache.set(key, code, timeout=settings.OTP_CODE_TTL_SECONDS)


def get_otp_code(phone: str) -> str | None:
    """
    Retrieve stored OTP code from cache.
    """
    return cache.get(get_otp_cache_key(phone))


def delete_otp_code(phone: str) -> None:
    """
    Delete OTP code after usage.
    """
    cache.delete(get_otp_cache_key(phone))


def is_rate_limited(phone: str) -> bool:
    """
    Check if OTP was recently sent to enforce rate limiting.
    """
    return cache.get(f"otp_rate_limit:{phone}") is not None


def set_rate_limit(phone: str) -> None:
    """
    Set rate limit for a phone number.
    """
    cache.set(f"otp_rate_limit:{phone}", "1", timeout=settings.OTP_RATE_LIMIT_SECONDS)
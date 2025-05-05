import hashlib
import secrets

def hash_password(password: str, salt: bytes = None) -> str:
    """Генерация безопасного хеша пароля"""
    salt = salt or secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000  # Количество итераций
    )
    return f"{salt.hex()}:{key.hex()}"
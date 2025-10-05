from app.settings import settings

def encrypt_password(password: str) -> str:
    return settings.fernet.encrypt(password.encode("utf-8")).decode("utf-8")


def decrypt_password(password: str) -> str:
    return settings.fernet.decrypt(password.encode("utf-8")).decode("utf-8")
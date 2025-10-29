from email.utils import parseaddr

from app.exceptions.api import (
    EmailIsTooLong,
    InvalidEmail,
    InvalidNickname,
)


def is_valid_email(email: str) -> bool:
    try:
        parsed_email = parseaddr(email)[1]
        return "@" in parsed_email and "." in parsed_email.split("@")[1]
    except Exception:
        return False

def check_email_length(email: str) -> bool:
    return len(email) <= 256

def check_nickname(nickname: str) -> bool:
    return 3 <= len(nickname) <= 50 and nickname.isalnum()

def check_user(email: str, nickname: str):
    if not is_valid_email(email):
        raise InvalidEmail
    if not check_email_length(email):
        raise EmailIsTooLong
    if not check_nickname(nickname):
        raise InvalidNickname

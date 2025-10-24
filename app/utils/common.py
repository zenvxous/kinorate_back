from email.utils import parseaddr


def is_valid_email(email: str) -> bool:
    try:
        parsed_email = parseaddr(email)[1]
        return "@" in parsed_email and "." in parsed_email.split("@")[1]
    except Exception:
        return False

from app.exceptions.base import AppException


class InvalidEmail(AppException):
    def __init__(self, message="Invalid format for email.", details: dict = None):
        if details is None:
            details = {"error": "Invalid format for email."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class UserAlreadyExists(AppException):
    def __init__(self, message="User already exists.", details: dict = None):
        if details is None:
            details = {"error": "User with this email or nickname already exists."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class InvalidCredentials(AppException):
    def __init__(self, message="Invalid email or password.", details: dict = None):
        if details is None:
            details = {"error": "Invalid email or password."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class InvalidFormData(AppException):
    def __init__(self, message="Invalid form data.", details: dict = None):
        if details is None:
            details = {"error": "Invalid form data."}
        super().__init__(message, code="UNPROCESSABLE_ENTITY", status_code=422, details=details)

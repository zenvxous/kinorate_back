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

class Unauthorized(AppException):
    def __init__(self, message="Unauthorized access.", details: dict = None):
        if details is None:
            details = {"error": "Unauthorized access."}
        super().__init__(message, code="UNAUTHORIZED", status_code=401, details=details)

class UserDoesntExists(AppException):
    def __init__(self, message="User doesn't exist.", details: dict = None):
        if details is None:
            details = {"error": "User doesn't exist."}
        super().__init__(message, code="NOT_FOUND", status_code=404, details=details)

class Forbidden(AppException):
    def __init__(self, message="Forbidden access.", details: dict = None):
        if details is None:
            details = {"error": "Forbidden access."}
        super().__init__(message, code="FORBIDDEN", status_code=403, details=details)

class UserEmailOrNicknameAlreadyExists(AppException):
    def __init__(self, message="User email or nickname already exists.", details: dict = None):
        if details is None:
            details = {"error": "User with this email or nickname already exists."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class NoChangesError(AppException):
    def __init__(self, message="No changes detected.", details: dict = None):
        if details is None:
            details = {"error": "No changes detected in update request."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class MovieAlreadyExists(AppException):
    def __init__(self, message="Movie already exists.", details: dict = None):
        if details is None:
            details = {"error": "Movie with this TMDB ID already exists."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class InvalidMovieStatus(AppException):
    def __init__(self, message="Invalid movie status.", details: dict = None):
        if details is None:
            details = {"error": "Invalid movie status provided."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class MovieNotFound(AppException):
    def __init__(self, message="Movie not found.", details: dict = None):
        if details is None:
            details = {"error": "Movie not found."}
        super().__init__(message, code="NOT_FOUND", status_code=404, details=details)

class InvalidRate(AppException):
    def __init__(self, message="Invalid rate value.", details: dict = None):
        if details is None:
            details = {"error": "Rate must be between 0 and 10."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class InvalidMovieGenres(AppException):
    def __init__(self, message="Invalid movie genres.", details: dict = None):
        if details is None:
            details = {"error": "One or more provided genres are invalid."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class InvalidComment(AppException):
    def __init__(self, message="Invalid comment.", details: dict = None):
        if details is None:
            details = {"error": "Comment exceeds maximum length of 2000 characters."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class RecentionNotFound(AppException):
    def __init__(self, message="Recention not found.", details: dict = None):
        if details is None:
            details = {"error": "Recention not found."}
        super().__init__(message, code="NOT_FOUND", status_code=404, details=details)

class InvalidNickname(AppException):
    def __init__(self, message="Invalid nickname.", details: dict = None):
        if details is None:
            details = {"error": "Nickname must be 3-50 characters long and alphanumeric."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

class EmailIsTooLong(AppException):
    def __init__(self, message="Email is too long.", details: dict = None):
        if details is None:
            details = {"error": "Email must not exceed 256 characters."}
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)

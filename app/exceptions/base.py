import logging


class AppException(Exception):
    def __init__(self, message: str, code: str = "APP_ERROR", status_code: int = 400, details: dict = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self):
        return {"message": self.message, "code": self.code, "status_code": self.status_code, "details": self.details}

    def log(self, logger: logging.Logger):
        level = logging.ERROR if self.status_code >= 500 else logging.WARNING
        logger.log(
            level,
            f"[{self.code}] {self.message}",
            extra={
                "status": self.status_code,
                "details": self.details,
                "code": self.code,
            },
        )

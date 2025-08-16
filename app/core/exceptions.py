from fastapi import Request
from fastapi.responses import JSONResponse


class SkillMatchException(Exception):
    """
    Base exception class for Skill Match exceptions.
    """

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

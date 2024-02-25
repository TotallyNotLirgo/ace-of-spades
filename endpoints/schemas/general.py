from dataclasses import dataclass
from fastapi import HTTPException


@dataclass
class BasicResponse:
    message: str = "OK"


class APIError(HTTPException):
    def __init__(self,
                 status_code: int,
                 error_message: str = "Unknown error") -> None:
        super().__init__(status_code, detail={"error": error_message})

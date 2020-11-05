from dataclasses import dataclass
from enum import Enum


# noinspection PyPep8Naming
class HTTP_STATUS(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found."
    SERVER_ERROR = "500 Internal Server Error"


@dataclass
class Response:
    status: HTTP_STATUS
    headers: dict
    body: bytes

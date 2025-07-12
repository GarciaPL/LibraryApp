from enum import StrEnum


class BookStatus(StrEnum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

    @classmethod
    def is_valid_status(cls, status: str) -> bool:
        return status.strip().lower() in [e.value for e in cls] if status else False

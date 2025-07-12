from enum import StrEnum


class UserType(StrEnum):
    User = "user"
    Staff = "staff"

    @classmethod
    def is_valid_usertype(cls, user_type: str) -> bool:
        return (
            user_type.strip().lower() in [e.value for e in cls] if user_type else False
        )

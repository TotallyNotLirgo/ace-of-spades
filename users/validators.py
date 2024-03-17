from email_validator import EmailNotValidError
from email_validator import validate_email as validate_e

from .security import hash_value


def validate_username(v: str) -> str:
    if len(v) < 4:
        raise ValueError("Username must be at least 4 characters long")
    if len(v) > 32:
        raise ValueError("Username must be at most 32 characters long")
    if not v.replace("_", "").isalnum():
        raise ValueError(
            "Username must contain only letters, numbers and underscores"
        )
    return v


def validate_password(v: str) -> str:
    special = "!@#$%^&*()-_=+[{]}\\|;:'\",<."
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if len(v) > 32:
        raise ValueError("Password must be at most 32 characters long")
    if not any(c.isdigit() for c in v):
        raise ValueError("Password must contain at least 1 digit")
    if not any(c.isupper() for c in v):
        raise ValueError("Password must contain at least 1 uppercase letter")
    if not any(c.islower() for c in v):
        raise ValueError("Password must contain at least 1 lowercase letter")
    if not any(c in special for c in v):
        raise ValueError("Password must contain at least 1 special character")
    if not all((c.isalnum() or c in special) for c in v):
        raise ValueError(f"Special characters allowed are: {special}")
    return hash_value(v)


def validate_email(v: str) -> str:
    try:
        return validate_e(v, check_deliverability=False).normalized
    except EmailNotValidError as e:
        raise ValueError(str(e))

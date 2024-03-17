import pytest

from users.validators import (
    validate_email,
    validate_password,
    validate_username,
)


def test_validate_username():
    assert validate_username("user") == "user"
    with pytest.raises(ValueError) as err:
        validate_username("use")
    assert err.value.args[0] == "Username must be at least 4 characters long"
    with pytest.raises(ValueError) as err:
        validate_username("u" * 33)
    assert err.value.args[0] == "Username must be at most 32 characters long"
    with pytest.raises(ValueError) as err:
        validate_username("user!")
    assert (
        err.value.args[0]
        == "Username must contain only letters, numbers and underscores"
    )


def test_validate_password():
    assert len(validate_password("Password123!")) == 64
    with pytest.raises(ValueError) as err:
        validate_password("Pas123!")
    assert err.value.args[0] == "Password must be at least 8 characters long"
    with pytest.raises(ValueError) as err:
        validate_password("Password12!" * 3)
    assert err.value.args[0] == "Password must be at most 32 characters long"
    with pytest.raises(ValueError) as err:
        validate_password("Password123")
    assert (
        err.value.args[0]
        == "Password must contain at least 1 special character"
    )
    with pytest.raises(ValueError) as err:
        validate_password("password123!")
    assert (
        err.value.args[0]
        == "Password must contain at least 1 uppercase letter"
    )
    with pytest.raises(ValueError) as err:
        validate_password("PASSWORD123!")
    assert (
        err.value.args[0]
        == "Password must contain at least 1 lowercase letter"
    )
    with pytest.raises(ValueError) as err:
        validate_password("Password!!!")
    assert err.value.args[0] == "Password must contain at least 1 digit"
    with pytest.raises(ValueError) as err:
        validate_password("Password123!🦝")
    assert (
        err.value.args[0]
        == "Special characters allowed are: !@#$%^&*()-_=+[{]}\\|;:'\",<."
    )


def test_validate_email():
    assert validate_email("email@email.com") == "email@email.com"
    with pytest.raises(ValueError) as err:
        validate_email("email")
    assert (
        err.value.args[0]
        == "The email address is not valid. It must have exactly one @-sign."
    )
    with pytest.raises(ValueError) as err:
        validate_email("email@")
    assert err.value.args[0] == "There must be something after the @-sign."
    with pytest.raises(ValueError) as err:
        validate_email("email@email")
    assert (
        err.value.args[0]
        == "The part after the @-sign is not valid. It should have a period."
    )
    with pytest.raises(ValueError) as err:
        validate_email("email@.com")
    assert (
        err.value.args[0]
        == "An email address cannot have a period "
            "immediately after the @-sign."
    )
    with pytest.raises(ValueError) as err:
        validate_email("email@email.")
    assert err.value.args[0] == "An email address cannot end with a period."

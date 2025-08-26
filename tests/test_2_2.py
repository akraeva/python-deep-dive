import pytest
from module_2 import UsernameValidator, PasswordValidator, User


@pytest.mark.parametrize(
    "username", [("validName"), ("user_123"), ("validUser1"), ("valid_name_1")]
)
def test_valid_username(username):
    user = User(username, "ValidPass123")
    assert user.username == username


@pytest.mark.parametrize(
    "username, expected_error",
    [
        ("123user", "Username must start with a letter"),
        ("ab", "Username must be between 3 and 20 characters"),
        ("a" * 21, "Username must be between 3 and 20 characters"),
        ("user@name", "Username can contain only letters, digits, and underscores"),
        (123, "Username must be a string"),
    ],
)
def test_invalid_username(username, expected_error):
    with pytest.raises(ValueError) as excinfo:
        User(username, "ValidPass123")
    assert str(excinfo.value) == expected_error


@pytest.mark.parametrize(
    "password", [("ValidPass123"), ("Password1"), ("SuperSecure123")]
)
def test_valid_password(password):
    user = User("valid_user", password)
    assert user.password == password


@pytest.mark.parametrize(
    "password, expected_error",
    [
        ("short", "Password must be at least 8 characters long"),
        ("missingupper123", "Password must contain at least one uppercase letter"),
        ("MISSINGLOWERCASE123", "Password must contain at least one lowercase letter"),
        ("NoDigitsHere", "Password must contain at least one digit"),
        (12345, "Password must be a string"),
    ],
)
def test_invalid_password(password, expected_error):
    with pytest.raises(ValueError) as excinfo:
        user = User("valid_user", password)
    assert str(excinfo.value) == expected_error


def test_username_validator_methods():
    username_validator = UsernameValidator()
    assert hasattr(
        username_validator, "__get__"
    ), "UsernameValidator should have '__get__' method"
    assert hasattr(
        username_validator, "__set__"
    ), "UsernameValidator should have '__set__' method"


def test_password_validator_methods():
    password_validator = PasswordValidator()
    assert hasattr(
        password_validator, "__get__"
    ), "PasswordValidator should have '__get__' method"
    assert hasattr(
        password_validator, "__set__"
    ), "PasswordValidator should have '__set__' method"

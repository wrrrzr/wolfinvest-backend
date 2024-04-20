import pytest

from app.utils.jwt import (
    hash_password,
    verify_password,
    create_jwt_token,
    verify_jwt_token,
)


@pytest.mark.parametrize("passwd", ["secretpassword", "12345678"])
def test_hash_password(passwd: str) -> None:
    pass_hash = hash_password(passwd)
    assert verify_password(passwd, pass_hash) is True


def test_hash_password_incorrect() -> None:
    pass_hash = hash_password("qwerty")
    assert verify_password("abcdef", pass_hash) is False


def test_create_jwt_token() -> None:
    token = create_jwt_token({"id": 5533})
    assert verify_jwt_token(token)["id"] == 5533


def test_incorrect_verify() -> None:
    assert verify_jwt_token("ashjkwerghjkmnbvc234671i6dfbnafv") is None

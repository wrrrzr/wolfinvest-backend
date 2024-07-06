import pytest

from app.adapters.auth import JWTAuthManager
from app.logic.models import JWTConfig


@pytest.fixture
def manager() -> JWTAuthManager:
    return JWTAuthManager(JWTConfig(auth_secret_key="SDFGHJKL"))


@pytest.fixture
def other_manager() -> JWTAuthManager:
    return JWTAuthManager(JWTConfig(auth_secret_key="wfghjdkflgsjh"))


async def test_hash_password(manager: JWTAuthManager) -> None:
    assert await manager.hash_password("Hello") != "Hello"


async def test_verify_password(manager: JWTAuthManager) -> None:
    passwd_hash = await manager.hash_password("secretpassword1")
    assert (
        await manager.verify_password("secretpassword1", passwd_hash) is True
    )


async def test_incorrect_verify_password(manager: JWTAuthManager) -> None:
    passwd_hash = await manager.hash_password("oldpassword")
    assert await manager.verify_password("newpassword", passwd_hash) is False


async def test_create_token(manager: JWTAuthManager) -> None:
    assert isinstance(await manager.create_token({"id": 1}), str) is True


async def test_verify_token(manager: JWTAuthManager) -> None:
    token = await manager.create_token({"id": 3})
    assert (await manager.verify_token(token))["id"] == 3


async def test_incorrect_verify_token(manager: JWTAuthManager) -> None:
    assert await manager.verify_token("asbhdfjkvwhjd") is None


async def test_incorrect_secret_key_token(
    manager: JWTAuthManager, other_manager: JWTAuthManager
) -> None:
    token = await manager.create_token({"id": 100})
    assert await other_manager.verify_token(token) is None

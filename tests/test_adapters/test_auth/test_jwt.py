import pytest

from app.adapters.auth import JWTTokenManager
from app.logic.models import JWTConfig


@pytest.fixture
def manager() -> JWTTokenManager:
    return JWTTokenManager(JWTConfig(auth_secret_key="SDFGHJKL"))


@pytest.fixture
def other_manager() -> JWTTokenManager:
    return JWTTokenManager(JWTConfig(auth_secret_key="wfghjdkflgsjh"))


async def test_create_token(manager: JWTTokenManager) -> None:
    assert isinstance(await manager.create_token({"id": 1}), str) is True


async def test_verify_token(manager: JWTTokenManager) -> None:
    token = await manager.create_token({"id": 3})
    assert (await manager.verify_token(token))["id"] == 3


async def test_incorrect_verify_token(manager: JWTTokenManager) -> None:
    assert await manager.verify_token("asbhdfjkvwhjd") is None


async def test_incorrect_secret_key_token(
    manager: JWTTokenManager, other_manager: JWTTokenManager
) -> None:
    token = await manager.create_token({"id": 100})
    assert await other_manager.verify_token(token) is None

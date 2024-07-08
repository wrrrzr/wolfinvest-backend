import pytest

from app.adapters.auth import PasslibPasswordManager


@pytest.fixture
def manager() -> PasslibPasswordManager:
    return PasslibPasswordManager()


async def test_hash_password(manager: PasslibPasswordManager) -> None:
    assert await manager.hash_password("Hello") != "Hello"


async def test_verify_password(manager: PasslibPasswordManager) -> None:
    passwd_hash = await manager.hash_password("secretpassword1")
    assert (
        await manager.verify_password("secretpassword1", passwd_hash) is True
    )


async def test_incorrect_verify_password(
    manager: PasslibPasswordManager,
) -> None:
    passwd_hash = await manager.hash_password("oldpassword")
    assert await manager.verify_password("newpassword", passwd_hash) is False

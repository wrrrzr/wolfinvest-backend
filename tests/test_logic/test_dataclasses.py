from dataclasses import dataclass

import pytest

from app.logic.dataclasses import object_to_dataclass, objects_to_dataclasses


class SomeClass:
    def __init__(self, a: int, b: str, c: float) -> None:
        self.a = a
        self.b = b
        self.c = c


@dataclass
class SomeDataclass:
    a: int
    b: str


@pytest.mark.parametrize(
    "a, b, c", [[10, "hello", 0.0], [14, "14", 1.5], [263891, "hwgdj", 10.33]]
)
def test_object_to_dataclass(a: int, b: str, c: float) -> None:
    some_object = SomeClass(a, b, c)
    assert object_to_dataclass(some_object, SomeDataclass) == SomeDataclass(
        a=a, b=b
    )


def test_objects_to_dataclasses() -> None:
    some_objects = (SomeClass(3, "hjkl", 5.1), SomeClass(111, "111", 111.1))
    assert objects_to_dataclasses(some_objects, SomeDataclass) == [
        SomeDataclass(3, "hjkl"),
        SomeDataclass(111, "111"),
    ]

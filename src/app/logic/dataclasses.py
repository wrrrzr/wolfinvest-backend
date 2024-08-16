from typing import Dict, Protocol, Any, Iterable


class ObjectWithDict(Protocol):
    __dict__: Dict[Any, Any]


def object_to_dataclass(obj: ObjectWithDict, dataclass: type[Any]) -> Any:
    data: Dict[Any, Any] = {}
    objdict = obj.__dict__
    need_data = tuple(dataclass.__dataclass_fields__.keys())
    for i in need_data:
        data[i] = objdict[i]
    return dataclass(**data)


def objects_to_dataclasses(
    objects: Iterable[ObjectWithDict], dataclass: type[Any]
) -> list[Any]:
    return [object_to_dataclass(i, dataclass) for i in objects]

from typing import Dict, Protocol, Any


class Dataclass(Protocol):
    __dataclass_fields__: Dict[str, Any]


class ObjectWithDict(Protocol):
    __dict__: Dict[Any, Any]


def object_to_dataclass(
    obj: ObjectWithDict, dataclass: type[Dataclass]
) -> Dataclass:
    data: Dict[Any, Any] = {}
    objdict = obj.__dict__
    need_data = tuple(dataclass.__dataclass_fields__.keys())
    for i in need_data:
        data[i] = objdict[i]
    return dataclass(**data)

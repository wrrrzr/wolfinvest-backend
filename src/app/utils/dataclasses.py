from typing import Dict, Protocol, Any


class ObjectWithDict(Protocol):
    __dict__: Dict[Any, Any]


def object_to_dataclass[T](obj: ObjectWithDict, dataclass: type[T]) -> T:
    data: Dict[Any, Any] = {}
    objdict = obj.__dict__
    need_data = tuple(dataclass.__dataclass_fields__.keys())
    for i in need_data:
        data[i] = objdict[i]
    return dataclass(**data)

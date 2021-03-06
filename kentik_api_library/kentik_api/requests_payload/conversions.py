import json
from enum import Enum
from typing import TypeVar, Type, Dict, Any, Optional, List, Iterable

import dacite

from kentik_api.public.errors import DeserializationError, DataFormatError


def as_dict(obj: Any) -> Dict[str, Any]:
    """ Convert obj to dict, removing all keys with None values """

    assert hasattr(obj, "__dict__") or isinstance(obj, dict), f"Input should be either class or dict , got: {type(obj)}"

    if hasattr(obj, "__dict__"):
        obj = obj.__dict__

    result = dict()
    for k, v in obj.items():
        if v is None:
            continue
        if isinstance(v, Enum):
            result[k] = v.value
        elif isinstance(v, list):
            result[k] = process_list(v)
        elif hasattr(v, "__dict__") or isinstance(v, dict):
            result[k] = as_dict(v)
        else:
            result[k] = v

    return result


def process_list(l: List[Any]) -> List[Any]:
    result = list()
    for item in l:
        if isinstance(item, Enum):
            result.append(item.value)
        elif hasattr(item, "__dict__") or isinstance(item, dict):
            result.append(as_dict(item))
        else:
            result.append(item)

    return result


T = TypeVar("T")
Data = Dict[str, Any]


def from_dict(data_class: Type[T], data: Data) -> T:
    """Converts given dictionary to the data class of given type. It converts Dacite errors into
    DeserializationError"""

    try:
        return dacite.from_dict(data_class=data_class, data=data)
    except dacite.DaciteError as err:
        raise DeserializationError(data_class.__name__, str(err)) from err


def from_json(class_name: str, json_string: str, root: str = "") -> Dict[str, Any]:
    """
    Decodes given JSON to a dictionary. It converts json errors into DeserializationError.
    root - use it to extract data that is nested under a root object e.g. "interface": {...}
    """

    try:
        return json.loads(json_string) if root == "" else json.loads(json_string)[root]
    except json.JSONDecodeError as err:
        raise DeserializationError(class_name, str(err)) from err
    except KeyError as err:
        raise DeserializationError(class_name, str(err)) from err


def convert(attr: Any, convert_func) -> Any:
    """ Convert input using convert_func. Raise DataFormatError on failure """

    try:
        return convert_func(attr)
    except Exception as err:
        raise DataFormatError(str(err)) from err


def convert_or_none(attr: Any, convert_func) -> Optional[Any]:
    """ Convert if input is not None, else just return None. Raise DataFormatError on failure  """

    if attr is None or attr == {}:
        return None
    return convert(attr, convert_func)


def convert_list_or_none(items: Optional[Iterable[Any]], convert_func) -> Optional[List[Any]]:
    """ Convert list if input list is not None, else just return None. Raise DataFormatError on failure  """

    if items is None:
        return None
    return [convert(item, convert_func) for item in items]


def enum_to_str(enum: Enum) -> str:
    """ Convert enum value to str. To be used with convert* functions """
    return str(enum.value)

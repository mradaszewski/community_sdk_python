# Standard library imports
import json
from typing import Optional, List, Any
from dataclasses import dataclass


@dataclass()
class GetResponse:

    id : int
    name: str
    color: str
    user_id: str
    company_id: str
    devices : List[Any]
    created_date : str
    updated_date : str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)


class GetAllResponse(List[GetResponse]):

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        labels = cls()
        for item in dic:
            l = GetResponse(**item)
            labels.append(l)
        return labels


@dataclass()
class CreateRequest:

    name: str # eg. "apitest-label-1"
    color: str # eg. "#00FF00"


@dataclass()
class CreateResponse:

    id : int
    name: str
    color: str
    user_id: str
    company_id: str
    devices : List[Any]
    created_date : str
    updated_date : str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)


@dataclass()
class UpdateRequest:

    name: str
    color: Optional[str] = None


@dataclass()
class UpdateResponse:

    id : int
    name: str
    color: str
    user_id: str
    company_id: str
    devices : List[Any]
    created_date : str
    updated_date : str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)


@dataclass()
class DeleteResponse:

    success: bool

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

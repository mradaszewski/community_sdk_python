from typing import List, Any, Optional

class DeviceLabel:

    @classmethod
    def for_create(cls, name: str, color: str):
        return cls(name, color, 0, "", "", [], "", "")

    @classmethod
    def for_update(cls, name: str, color: Optional[str] = None):
        return cls(name, color, 0, "", "", [], "", "")

    def __init__(self, name: str, color: Optional[str], id: int, user_id: str, company_id: str,
                    devices: List[Any], created_date: str, updated_date: str) -> None:
        # read-write
        self.name = name
        self.color = color

        # read-only
        self._id = id
        self._user_id = user_id
        self._company_id = company_id
        self._devices = devices
        self._created_date = created_date
        self._updated_date = updated_date


    @property
    def id(self) -> int:
        return self._id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def company_id(self) -> str:
        return self._company_id

    @property
    def devices(self) -> List[Any]:
        return self._devices

    @property
    def created_date(self) -> str:
        return self._created_date

    @property
    def updated_date(self) -> str:
        return self._updated_date

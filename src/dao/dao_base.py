from __future__ import annotations

import typing
from connectors import g_connector

if typing.TYPE_CHECKING:
    from typing import Dict, Type, List, Any


class DaoBase:
    def __init__(self, data: Dict) -> None:
        self._data = data

    def __dict__(self) -> Dict:
        return self._data

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def apply(self, destination: str):
        g_connector.insert(destination, self)

    @staticmethod
    def create_from_data_source(source: str, cls: Type[DaoBase]) -> DaoBase:
        data = g_connector.get_from(source, 1)
        return cls(data)

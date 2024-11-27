from __future__ import annotations

import json
import typing
from connectors import g_connector
from constants import DAO_CONFIGS

if typing.TYPE_CHECKING:
    from typing import Dict, Type, List, Any


class DaoConfig:
    def __init__(self, classname: str) -> None:
        self.classname = classname
        self.raw = self.get_config()

    def __getitem__(self, key: str) -> Any:
        return self.raw.get(key)

    def get_config(self) -> Dict[str, Any]:
        filename = DAO_CONFIGS + self.classname + '.json'

        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


class DaoBase:
    FIELDS = ('_classname', '_data', '__class__')
    CONFIGS = {}

    def __init__(self,data: Dict) -> None:
        classname = self.__class__.__name__
        if classname not in DaoBase.CONFIGS:
            DaoBase.CONFIGS[classname] = DaoConfig(classname)

        self._data = data
        self._classname = classname

    def __dict__(self) -> Dict:
        return self._data

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __getattribute__(self, item):
        if item in DaoBase.FIELDS:
            return super().__getattribute__(item)
        if item in DaoBase.CONFIGS[self._classname]['fields']:
            return super().__getattribute__('_data').get(item)
        return super().__getattribute__(item)

    def __setattr__(self, item, value):
        if item in DaoBase.FIELDS:
            return super().__setattr__(item, value)
        if item in DaoBase.CONFIGS[self._classname]['fields']:
            super().__getattribute__('_data')[item] = value
            return
        return super().__setattr__(item, value)

    def apply(self, destination: str):
        g_connector.insert(destination, self)

    @staticmethod
    def create_from_data_source(source: str, cls: Type[DaoBase]) -> DaoBase:
        data = g_connector.get_from(source, 1)
        return cls(data)

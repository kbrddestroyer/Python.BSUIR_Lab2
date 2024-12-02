from __future__ import annotations

import json
import typing
from connectors import g_connector
from constants import DAO_CONFIGS

if typing.TYPE_CHECKING:
    from typing import Dict, Type, Any


class DaoConfig:
    def __init__(self, classname: str) -> None:
        self.classname = classname
        self.raw = self.get_config()

    def __getitem__(self, key: str) -> Any:
        return self.raw.get(key)

    def get_config(self) -> Dict[str, Any]:
        filename = DAO_CONFIGS + self.classname + ".json"

        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


class DaoBase:
    CONFIGS = {}

    def __init__(self, data: Dict) -> None:
        classname = self.__class__.__name__
        if classname not in DaoBase.CONFIGS:
            DaoBase.CONFIGS[classname] = DaoConfig(classname)

        self._fields = DaoBase.CONFIGS[classname]['fields']
        self._data = data

        for k, v in self._fields.items():
            if k not in self._data:
                self._data[k] = v

        self._classname = classname
        self._primary_key = DaoBase.CONFIGS[classname]['primary']

    @property
    def primary_key(self):
        return self._data[self._primary_key]

    def __dict__(self) -> Dict:
        return self._data

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __getattribute__(self, item):
        if item[0] == '_':
            return super().__getattribute__(item)
        if item in self._fields:
            return super().__getattribute__("_data").get(item)
        return super().__getattribute__(item)

    def __setattr__(self, item, value):
        if item[0] == '_':
            return super().__setattr__(item, value)
        if item in self._fields:
            super().__getattribute__("_data")[item] = value
            return
        return super().__setattr__(item, value)

    def apply(self):
        config = DaoBase.CONFIGS[self._classname]
        g_connector.insert(config['table'], self)

    def delete_self(self):
        config = DaoBase.CONFIGS[self._classname]
        g_connector.remove(config['table'], self.primary_key)

    @staticmethod
    def create_from_data_source(source: str, cls: Type[DaoBase], is_single: bool = False) -> DaoBase or Dict[Any, DaoBase]:
        data = g_connector.get_from(source)
        objects = {}

        if not data:
            return None

        if is_single:
            return cls(data)

        for key, init_data in data.items():
            dao = cls(init_data)
            objects[key] = dao
        return objects

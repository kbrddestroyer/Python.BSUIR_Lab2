from __future__ import annotations

import typing
import json

from typing import override
from connectors import connector_base
from entities import entity

if typing.TYPE_CHECKING:
    from typing import Any, Optional, Dict
    from dao import dao_base


class JsonConnector(connector_base.ConnectorBase):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.__filename = filename
        self.__file = JsonConnector.__open_file(filename)
        self.__data = self.__prepare_data()

    @override
    def finish(self) -> None:
        self.__save_data()

    @staticmethod
    def __open_file(filename):
        try:
            return open(filename, "r")
        except FileNotFoundError:
            return None

    def __prepare_data(self) -> Dict:
        if not self.__file:
            return {}

        try:
            return json.load(self.__file)
        except json.decoder.JSONDecodeError:
            return {}

    def __save_data(self) -> None:
        entity.finalize_all()

        if self.__file:
            self.__file.close()
        with open(self.__filename, 'w') as f:
            json.dump(self.__data, indent=4, fp=f)

    @override
    def read(self, key: str) -> Any:
        keys = key.split('/')
        data = self.__data
        for k in keys:
            if k not in data:
                return {}
            data = data[k]
        return data

    @override
    def write(self, key, pk, value) -> None:
        if key not in self.__data:
            self.__data[key] = {}
        self.__data[key][pk] = value

    @override
    def get_from(self, source: str, limit: Optional[int] = None) -> Any:
        data = self.read(source)
        if not limit or not data:
            return data
        return data[: limit if limit <= len(data) else len(data)]

    @override
    def insert(self, destination: str, dao: dao_base.DaoBase) -> None:
        self.write(destination, dao.primary_key, dao.__dict__())

    @override
    def remove(self, destination: str, key: dao_base):
        if key in self.__data.get(destination, {}):
            self.__data[destination].pop(key)

    def __getitem__(self, key: str) -> Any:
        return self.__data.get(key, None)

    def __setitem__(self, key: str, value) -> None:
        self.__data[key] = value

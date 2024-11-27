from __future__ import annotations

import typing
import json

from typing import override
from connectors import connector_base

if typing.TYPE_CHECKING:
    from typing import Any, Optional, Dict


class JsonConnector(connector_base.ConnectorBase):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)

        self.__file = JsonConnector.__open_file(filename)

        if self.__file:
            self.__data = self.__prepare_data()

    def __del__(self) -> None:
        if self.__file:
            self.__save_data()
            self.__file.close()

    @staticmethod
    def __open_file(filename):
        try:
            file = open(filename, "w+")
        except FileNotFoundError:
            JsonConnector.__try_create_file(filename)
            file = open(filename, "w+")
        assert file
        return file

    @staticmethod
    def __try_create_file(filename: str) -> None:
        with open(filename, "w") as _:
            pass

    def __prepare_data(self) -> Dict:
        try:
            return json.load(self.__file)
        except json.decoder.JSONDecodeError:
            return {}

    def __save_data(self) -> None:
        if self.__file:
            self.__file.write(json.dumps(self.__data, indent=4))

    @override
    def read(self, key) -> Any:
        return self.__data.get(key, {})

    @override
    def write(self, key, value) -> None:
        self.__data[key] = value

    @override
    def get_from(self, source: str, limit: Optional[int] = None) -> Any:
        data = self.read(source)
        if not limit or not data:
            return data
        return data[: limit if limit <= len(data) else len(data)]

    @override
    def insert(self, destination: str, dao: Any) -> None:
        self.write(destination, dao.__dict__())

    def __getitem__(self, key: str) -> Any:
        return self.__data.get(key, None)

    def __setitem__(self, key: str, value) -> None:
        self.__data[key] = value

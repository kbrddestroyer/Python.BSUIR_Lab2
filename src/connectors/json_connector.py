from __future__ import annotations

import typing
import json

from typing import override
from connectors import connector_base

if typing.TYPE_CHECKING:
    from typing import Any, Optional


class JsonConnector(connector_base.ConnectorBase):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)

        try:
            self.__file = open(filename, 'r+')
        except FileNotFoundError:
            self.__file = None

        if self.__file:
            self.__data = self.__prepare_data()

    def __del__(self) -> None:
        if self.__file:
            self.__save_data()
            self.__file.close()

    def __prepare_data(self) -> Optional[dict]:
        try:
            return json.load(self.__file)
        except json.decoder.JSONDecodeError:
            return None

    def __save_data(self) -> None:
        self.__file.write(json.dumps(self.__data))

    @override
    def read(self, key) -> Any:
        return self.__data.get(key, None)

    @override
    def write(self, key, value) -> None:
        self.__data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.__data.get(key, None)

    def __setitem__(self, key: str, value) -> None:
        self.__data[key] = value

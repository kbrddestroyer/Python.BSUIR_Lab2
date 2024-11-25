from __future__ import annotations

import typing
import configparser

from abc import abstractmethod
from constants import CONNECTOR_CONFIG

if typing.TYPE_CHECKING:
    from typing import Any


g_connector = None


class ConnectorBase:
    """
    Base class for DB and FILE IO connectivity. Contains `read(...)` and `write(...)` methods that should be implemented
    in derived classes
    """

    def __init__(self, source: Any):
        self.__source = source

    @abstractmethod
    def read(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def write(self, *args, **kwargs) -> None:
        raise NotImplementedError


def get_global_connector() -> None:
    global g_connector

    config = configparser.ConfigParser()
    config.read(CONNECTOR_CONFIG)

    connector_class = config['CONNECTOR_CLASS']['connector']
    classes = ConnectorBase.__subclasses__()
    for connector in classes:
        if connector_class == connector:
            assert False


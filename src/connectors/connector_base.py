from __future__ import annotations

import typing
import configparser

from abc import abstractmethod
from constants import CONNECTOR_CONFIG

if typing.TYPE_CHECKING:
    from typing import Any


global __g_connector


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
    global __g_connector

    from connectors import create_connectors

    config = configparser.ConfigParser()
    config.read(CONNECTOR_CONFIG)

    connector_class = config['CONNECTOR_CLASS']['connector']
    source = config['CONNECTOR_CLASS']['source']

    subclasses = create_connectors()
    for connector in subclasses:
        if connector_class == connector.__name__:
            __g_connector = connector(source)
            return


@property
def g_connector():
    global __g_connector
    return __g_connector

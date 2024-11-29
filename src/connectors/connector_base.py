from __future__ import annotations

import typing
import configparser

from abc import abstractmethod
from constants import CONNECTOR_CONFIG

if typing.TYPE_CHECKING:
    from typing import Any, Optional


global g_connector


class ConnectorBase:
    """
    Base class for DB and FILE IO connectivity. Contains `read(...)` and `write(...)` methods that should be implemented
    in derived classes
    """

    def __init__(self, source: Any):
        self._source = source

    @abstractmethod
    def read(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def write(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_from(self, source: str, limit: Optional[int] = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def insert(self, destination: str, dao: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, destination: str, key: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def finish(self):
        raise NotImplementedError

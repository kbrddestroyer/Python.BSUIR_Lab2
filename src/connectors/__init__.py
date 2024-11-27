from __future__ import annotations

import typing
import configparser

from constants import CONNECTOR_CONFIG
from connectors import connector_base
from connectors import json_connector


if typing.TYPE_CHECKING:
    from typing import Optional
    from connectors.connector_base import ConnectorBase


def _create_g_connector() -> Optional[ConnectorBase]:
    config = configparser.ConfigParser()
    config.read(CONNECTOR_CONFIG)

    connector_class = config["CONNECTOR_CLASS"]["connector"]
    source = config["CONNECTOR_CLASS"]["source"]

    subclasses = connector_base.ConnectorBase.__subclasses__()
    for connector in subclasses:
        if connector_class == connector.__name__:
            return connector(source)

    return None


g_connector = _create_g_connector()

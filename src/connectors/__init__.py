from __future__ import annotations

import typing

from connectors import connector_base
from connectors import json_connector


if typing.TYPE_CHECKING:
    from typing import List, Type


def create_connectors() -> List[Type]:
    subclasses = connector_base.ConnectorBase.__subclasses__()
    return subclasses

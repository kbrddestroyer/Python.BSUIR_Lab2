from __future__ import annotations

import typing

from dataclasses import dataclass
from entities import account
from connectors import g_connector

if typing.TYPE_CHECKING:
    from typing import Optional, List
    from account import Account


@dataclass
class Credentials:
    username: str
    password: str


class Login:
    def __init__(self):
        self.__accounts: List[Account] = []

    def try_login(self, credentials: Credentials) -> bool:
        g_connector.read()

from __future__ import annotations

import typing

from dataclasses import dataclass
from account import Account

if typing.TYPE_CHECKING:
    from typing import Optional, List


@dataclass
class Credentials:
    username: str
    password: str


class Login:
    def __init__(self):
        self.__accounts: List[Account] = []

    def try_login(self, credentials: Credentials) -> bool:
        pass

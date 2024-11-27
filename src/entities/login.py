from __future__ import annotations

import typing

from dataclasses import dataclass
from entities import account
from dao import account_dao
from connectors import g_connector

if typing.TYPE_CHECKING:
    from typing import Optional, List
    from account import Account


@dataclass
class Credentials:
    username: str
    password: str


class LOGIN_RESULT:
    SUCCESS = 0
    INVALID_USERNAME = 1
    INVALID_PASSWORD = 2


class Login:
    def try_login(self, credentials: Credentials) -> (int, Optional[account.Account]):
        fetched = account_dao.AccountDao.create_from_data_source(
            f"account/{credentials.username}", account_dao.AccountDao, True
        )
        if not fetched:
            return LOGIN_RESULT.INVALID_USERNAME, None

        hashed_password = account.hash_password(credentials.password)

        if hashed_password != fetched.password:
            return LOGIN_RESULT.INVALID_PASSWORD, None

        acc = account.Account()
        acc.from_dao(fetched)

        return LOGIN_RESULT.SUCCESS, acc

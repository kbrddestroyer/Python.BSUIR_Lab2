from __future__ import annotations

import typing

from dataclasses import dataclass
from entities import account
from dao import account_dao

if typing.TYPE_CHECKING:
    from typing import Optional


@dataclass
class Credentials:
    username: str
    password: str


class LOGIN_RESULT:
    SUCCESS = 0
    INVALID_USERNAME = 1
    INVALID_PASSWORD = 2


class REGISTER_RESULT:
    SUCCESS = 0
    INVALID_USERNAME = 1


class Login:
    @staticmethod
    def try_login(credentials: Credentials) -> (int, Optional[account.Account]):
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

    @staticmethod
    def try_register(credentials: Credentials) -> (int, Optional[account.Account]):
        fetched = account_dao.AccountDao.create_from_data_source(
            f"account/{credentials.username}", account_dao.AccountDao, True
        )

        if fetched.__dict__():
            return REGISTER_RESULT.INVALID_USERNAME, None

        acc = account.Account()
        acc.username = credentials.username
        acc.password = credentials.password

        acc.to_dao().apply("account")

        return REGISTER_RESULT.SUCCESS, acc

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


class AccountController:
    @staticmethod
    def fetch_account_by_username(username: str) -> account_dao.AccountDao:
        return account_dao.AccountDao.create_from_data_source(
            f'accounts/{username}', account_dao.AccountDao, True
        )

    @staticmethod
    def try_login(credentials: Credentials) -> (int, Optional[account.Account]):
        fetched = AccountController.fetch_account_by_username(credentials.username)
        if not fetched:
            return LOGIN_RESULT.INVALID_USERNAME, None

        hashed_password = account.hash_password(credentials.password)

        if hashed_password != fetched.password:
            return LOGIN_RESULT.INVALID_PASSWORD, None

        acc = account.Account(fetched)

        return LOGIN_RESULT.SUCCESS, acc

    @staticmethod
    def try_register(credentials: Credentials) -> (int, Optional[account.Account]):
        fetched = AccountController.fetch_account_by_username(credentials.username)

        if fetched:
            return REGISTER_RESULT.INVALID_USERNAME, None

        acc = account.Account()
        acc.username = credentials.username
        acc.password = credentials.password

        acc.save()

        return REGISTER_RESULT.SUCCESS, acc

    @staticmethod
    def try_delete(credentials: Credentials) -> bool:
        fetched = AccountController.fetch_account_by_username(credentials.username)

        if not fetched.__dict__():
            print('No entity')
            return False
        hashed = account.hash_password(credentials.password)
        if fetched.password != hashed:
            return False

        fetched.delete_self()
        return True

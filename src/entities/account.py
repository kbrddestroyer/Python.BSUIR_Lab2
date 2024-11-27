from __future__ import annotations

import typing

from hashlib import md5
from entities import entity

from dao import account_dao

if typing.TYPE_CHECKING:
    from typing import Optional, Any


class HashedValue:
    """
    Automatically converts variable to md5 hash
    """

    def __init__(self) -> None:
        self.__name = None

    def __set_name__(self, owner: Any, name: str) -> None:
        self.__name = f"_{owner.__name__}__{name}_desc"

    def __get__(self, instance: Any, _: type = None) -> Any:
        return getattr(instance, self.__name)

    def __set__(self, instance, value: Any) -> None:
        value = md5(value.encode("utf-8")).hexdigest()
        setattr(instance, self.__name, value)


class Account(entity.Entity):
    """
    Account entity contains basic user data, handles password hashing process
    Used in role management system. Derived from Entity

    - `self.id`: Unique ID (int)
    - `self.username`: username (str or None)
    - `self.password`: password (str or None)
    """

    __password_helper = HashedValue()

    def __init__(self):
        super().__init__()

        self.__username: Optional[str] = None

    def from_dao(self, dao: account_dao.AccountDao):
        self.__username = dao.username
        self.__password_helper = dao.password

    def to_dao(self) -> account_dao.AccountDao:
        data = {
            'username': self.__username,
            'password': self.__password_helper
        }
        return account_dao.AccountDao(data)

    @property
    def username(self) -> Optional[str]:
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @property
    def password(self) -> Optional[str]:
        return self.__password_helper

    @password.setter
    def password(self, password: str) -> None:
        self.__password_helper = password

    def __str__(self):
        return f"Account {self.__username}:{self.id}"

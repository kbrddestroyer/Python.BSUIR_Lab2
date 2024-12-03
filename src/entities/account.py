from __future__ import annotations

import typing
import tkinter

from typing import override

from hashlib import md5
from entities import entity, user_data

from dao import account_dao
from constants import ACCOUNTS

if typing.TYPE_CHECKING:
    from typing import Optional, Any


def hash_password(password: str) -> str:
    return md5(password.encode("utf-8")).hexdigest()


class HashedValue:
    """
    Automatically converts variable to md5 hash
    """

    def __init__(self, name: str = None) -> None:
        self.__name = name

    def __set_name__(self, owner: Any, name: str) -> None:
        if not self.__name:
            self.__name = f"_{owner.__name__}__{name}_desc"

    def __get__(self, instance: Any, _: type = None) -> Any:
        return getattr(instance, self.__name)

    def __set__(self, instance, value: Any) -> None:
        value = hash_password(value)
        setattr(instance, self.__name, value)


class Account(entity.Entity):
    """
    Account entity contains basic user data, handles password hashing process
    Used in role management system. Derived from Entity

    - `self.id`: Unique ID (int)
    - `self.username`: username (str or None)
    - `self.password`: password (str or None)
    """

    __password_helper = HashedValue('_Account__password')

    def __init__(self, dao: Optional[account_dao.AccountDao] = None):
        if not dao:
            dao = account_dao.AccountDao({})
        self.from_dao(dao)
        super().__init__()

    @override
    def from_dao(self, dao: account_dao.AccountDao):
        self.__username = dao.username
        self.__password = dao.password
        self.__type = dao.type
        self.__flags = dao.flags
        self.__user_data = user_data.UserData(self)

    @override
    def to_dao(self) -> account_dao.AccountDao:
        data = {
            'username': self.__username,
            'password': self.__password,
            'type': self.__type,
            'flags': self.__flags
        }
        return account_dao.AccountDao(data)

    @property
    def type(self):
        return self.__type

    @property
    def flags(self):
        return self.__flags

    @flags.setter
    def flags(self, flags: int):
        self.__flags = flags

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

    @override
    def save(self):
        self.__user_data.save()
        super().save()

    @override
    def create_widget(self, window: tkinter.Tk):
        self.__user_data.create_widget(window)

    def __str__(self):
        return f"Account {self.__username}:{self.id}"

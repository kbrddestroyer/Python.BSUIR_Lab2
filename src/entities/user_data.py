from __future__  import annotations

import typing
import tkinter

from typing import override

from dao import user_data_dao, dao_base
from entities import entity

if typing.TYPE_CHECKING:
    from entities import account


class UserData(entity.Entity):
    def __init__(self, acc: account.Account):
        dao = dao_base.DaoBase.create_from_data_source(
            f'user_data/{acc.username}',
            user_data_dao.UserDataDao, True
        )

        if not dao:
            # Create default
            dao = user_data_dao.UserDataDao({})

        self.from_dao(dao)
        self.__username = acc.username
        super().__init__()

    @override
    def from_dao(self, dao: dao_base) -> None:
        self.__username = dao.username
        self.__name = dao.name
        self.__phone = dao.phone
        self.__email = dao.email
        self.__address = dao.address
        self.__photo = dao.photo
        self.__birthday = dao.birthday

    @override
    def to_dao(self) -> dao_base:
        data = {
            "username": self.__username,
            "name": self.__name,
            "phone": self.__phone,
            "email": self.__email,
            "address": self.__address,
            "photo": self.__photo,
            "birthday": self.__birthday
        }

        return user_data_dao.UserDataDao(data)

    @override
    def create_widget(self, window: tkinter.Tk):
        from ui.gui.dao_widget import DaoWidget
        widget = DaoWidget(window)
        widget.set_dao(self.to_dao())
        widget.pack()

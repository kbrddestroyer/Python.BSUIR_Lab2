from __future__ import annotations

import typing

from typing import override

from dao import dao_base, message_dao
from entities import entity


class Message(entity.Entity):
    def __init__(self, dao: message_dao.MessageDao = None):
        if not dao:
            dao = message_dao.MessageDao({})
        self.from_dao(dao)

        super().__init__()

    @override
    def from_dao(self, dao: dao_base) -> None:
        self.__unique_id = dao.unique_id
        self.__username = dao.username
        self.__destination = dao.destination
        self.__message = dao.message
        self.__read = dao.read

    @override
    def to_dao(self) -> dao_base.DaoBase:
        data = {
            'unique_id': self.__unique_id,
            'username': self.__username,
            'destination': self.__destination,
            'message': self.__message,
            'read': self.__read
        }

        return message_dao.MessageDao(data)

    @override
    def create_widget(self, window, show_btn = True):
        from ui.gui.dao_widget import DaoWidget
        widget = DaoWidget(window)
        widget.set_dao(self.to_dao(), ['unique_id', 'username', 'read'], show_btn)
        widget.pack()

    @staticmethod
    def generate_id() -> int:
        result = dao_base.DaoBase.create_from_data_source(
            'messages', message_dao.MessageDao
        )
        if not result:
            return 0
        return len(result)
from __future__ import annotations

import typing
import tkinter
import time

from typing import override

from dao import dao_base, customer_dao
from entities import entity


class Customer(entity.Entity):
    def __init__(self, dao: customer_dao.CustomerDao = None):
        if not dao:
            dao = customer_dao.CustomerDao({})
        self.from_dao(dao)
        super().__init__()

    @override
    def from_dao(self, dao: customer_dao.CustomerDao) -> None:
        self.__unique_id = dao.unique_id
        self.__username = dao.username
        self.__timestamp = dao.timestamp
        self.__blood_pressure = dao.blood_pressure
        self.__pulse = dao.pulse

    @override
    def to_dao(self) -> dao_base.DaoBase:
        data = {
            'unique_id': self.__unique_id,
            'username': self.__username,
            'timestamp': self.__timestamp,
            'blood_pressure': self.__blood_pressure,
            'pulse': self.__pulse
        }

        return customer_dao.CustomerDao(data)

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @staticmethod
    def generate_id() -> int:
        result = dao_base.DaoBase.create_from_data_source(
            'customer_data', customer_dao.CustomerDao
        )
        if not result:
            return 0
        return len(result)

    @staticmethod
    def generate_timestamp() -> float:
        return time.time()

    @override
    def create_widget(self, window: tkinter.Tk, show_btn = True):
        from ui.gui.dao_widget import DaoWidget
        widget = DaoWidget(window)
        widget.set_dao(self.to_dao(), ['unique_id', 'username', 'timestamp'], show_btn)
        widget.pack()

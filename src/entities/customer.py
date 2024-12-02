from __future__ import annotations

import typing

from typing import override

from dao import dao_base, customer_dao
from entities import entity


class Customer(entity.Entity):
    def __init__(self, dao: customer_dao.CustomerDao = None):
        super().__init__()
        if not dao:
            dao = customer_dao.CustomerDao({})
        self.from_dao(dao)

    @override
    def from_dao(self, dao: customer_dao.CustomerDao) -> None:
        self.__username = dao.username
        self.__timestamp = dao.timestamp
        self.__blood_pressure = dao.blood_pressure
        self.__pulse = dao.pulse

    @override
    def to_dao(self) -> dao_base.DaoBase:
        data = {
            'username': self.__username,
            'timestamp': self.__timestamp,
            'blood_pressure': self.__blood_pressure,
            'pulse': self.__pulse
        }

        return customer_dao.CustomerDao(data)

    @override
    def create_widget(self, window):
        pass

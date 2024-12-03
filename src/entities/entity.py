from __future__ import annotations

import typing

from abc import abstractmethod

if typing.TYPE_CHECKING:
    from dao import dao_base


class Entity:
    G_ENTITIES = {}

    def __init__(self):
        self.__id = len(Entity.G_ENTITIES)
        Entity.G_ENTITIES[self.id] = self

    @property
    def id(self):
        return self.__id

    @abstractmethod
    def to_dao(self) -> dao_base.DaoBase:
        raise NotImplementedError

    @abstractmethod
    def from_dao(self, dao: dao_base) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_widget(self, window):
        pass

    def save(self):
        self.to_dao().apply()

    def destroy(self):
        Entity.G_ENTITIES.pop(self.__id)

    def finalize(self):
        pass

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if self in Entity.G_ENTITIES.values():
            self.save()

    def __str__(self):
        return f"Entity {self.id}"


def finalize_all():
    for entity in Entity.G_ENTITIES.values():
        entity.finalize()

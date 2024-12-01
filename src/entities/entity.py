class Entity:
    ENTITIES = 0

    def __init__(self):
        self.__id = Entity.ENTITIES
        Entity.ENTITIES += 1

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return f"Entity {self.id}"

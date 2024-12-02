from abc import abstractmethod


class UIBase:
    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def process_login(self):
        raise NotImplementedError

    @abstractmethod
    def process_register(self):
        raise NotImplementedError

    @abstractmethod
    def process_delete(self):
        raise NotImplementedError

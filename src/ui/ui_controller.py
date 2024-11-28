from __future__ import annotations

import typing
import configparser

from abc import abstractmethod
from constants import UI_CONFIG


class UIBase:
    def __init__(self):
        pass

    @abstractmethod
    def process_login(self):
        raise NotImplementedError

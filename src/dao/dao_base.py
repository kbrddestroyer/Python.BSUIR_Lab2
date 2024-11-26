from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    from typing import Dict


class DaoBase:
    def __init__(self, data: Dict) -> None:
        self.__keys = []
        for k, v in data.items():
            setattr(self, k, v)
            self.__keys.append(k)

    def __dict__(self) -> Dict:
        return {k: getattr(self, k) for k in self.__keys}

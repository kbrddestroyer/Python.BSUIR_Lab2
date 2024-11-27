from __future__ import annotations

import typing
from dao import dao_base


if typing.TYPE_CHECKING:
    from typing import Dict


class AccountDao(dao_base.DaoBase):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)

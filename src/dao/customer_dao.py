from __future__ import annotations

import typing

from dao import dao_base

if typing.TYPE_CHECKING:
    from typing import Dict


class CustomerDao(dao_base.DaoBase):
    def __init__(self, data: Dict):
        super().__init__(data)

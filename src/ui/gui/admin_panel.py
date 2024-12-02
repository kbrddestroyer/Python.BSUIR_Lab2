from __future__ import annotations

import typing
import tkinter

from constants import FLAGS
from typing import override

if typing.TYPE_CHECKING:
    from entities import account


class AdminPanel:
    @staticmethod
    def toggle_ban(acc: account.Account, button: tkinter.Button) -> None:
        acc.flags = FLAGS.ACCOUNT_BLOCKED if acc.flags != FLAGS.ACCOUNT_BLOCKED else FLAGS.NO_FLAGS
        acc.to_dao().apply()

        button.config(text=FLAGS.TO_BTN_LABEL[acc.flags])

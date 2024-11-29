from __future__ import annotations

import tkinter.messagebox

import tk
import typing

from ui import ui_controller
from controllers import account_controller
from typing import override


class GUIController(ui_controller.UIBase):
    def __init__(self):
        super().__init__()
        tkinter.messagebox.showinfo('Created GUI Controller')

    @override
    def process_login(self):
        pass

    @override
    def process_register(self):
        pass

    @override
    def process_delete(self):
        pass

from __future__ import annotations

import typing

from typing import override
from ui import ui_controller
from controllers import login


class CLIController(ui_controller.UIBase):
    def __init__(self):
        super().__init__()

    @override
    def process_login(self):
        username = input('> ')
        password = input('> ')

        credentials = login.Credentials(username, password)

        result, entity = login.Login.try_login(credentials)

        if not entity:
            print(f"Login invalid, error code: {result}")
            return

        print(f"Logged in as {entity.username}")
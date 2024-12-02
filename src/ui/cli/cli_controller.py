from __future__ import annotations

import typing

from ui import ui_controller
from controllers import account_controller

from typing import override


class CLIController(ui_controller.UIBase):
    def __init__(self):
        super().__init__()

    @override
    def start(self) -> None:
        pass

    @override
    def process_login(self):
        username = input('> ')
        password = input('> ')

        credentials = account_controller.Credentials(username, password)

        result, entity = account_controller.AccountController.try_login(credentials)

        if not entity:
            print(f"Login invalid, error code: {result}")
            return

        print(f"Logged in as {entity.username}")

    @override
    def process_register(self):
        username = input('> ')
        password = input('> ')

        credentials = account_controller.Credentials(username, password)
        result, entity = account_controller.AccountController.try_register(credentials)

        if not entity:
            print(f"Login invalid, error code: {result}")
            return

        print(f"Registered as {entity.username}")

        entity.to_dao().apply()

    @override
    def process_delete(self):
        username = input('> ')
        password = input('> ')

        credentials = account_controller.Credentials(username, password)
        result = account_controller.AccountController.try_delete(credentials)

        if not result:
            print(f"Removal invalid, error code: {result}")
            return

        print(f"Removed {credentials.username}")


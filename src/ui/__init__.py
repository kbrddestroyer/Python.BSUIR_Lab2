import configparser

import importlib

from ui import ui_controller
from constants import UI_CONFIG


def _create_controller() -> ui_controller.UIBase:
    config = configparser.ConfigParser()
    config.read(UI_CONFIG)

    mode = config['UI']['type']
    module = importlib.import_module(f'ui.{mode}')

    assert hasattr(module, 'create')
    return module.create()


g_ui_controller = _create_controller()

"""
Entrypoint
"""
from ui import g_ui_controller
from connectors import g_connector


def main():
    g_ui_controller.start()


if __name__ == "__main__":
    main()
    g_connector.finish()

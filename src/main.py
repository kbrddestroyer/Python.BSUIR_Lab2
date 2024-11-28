"""
Entrypoint
"""
from ui import g_ui_controller


def main():
    g_ui_controller.process_login()


if __name__ == "__main__":
    main()

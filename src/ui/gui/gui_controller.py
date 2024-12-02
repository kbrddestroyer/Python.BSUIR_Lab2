from __future__ import annotations

import tkinter.messagebox

import tkinter
import typing
import configparser
from functools import partial

from ui import ui_controller
from ui.gui import admin_panel
from controllers import account_controller
from typing import override
from constants import UI_CONFIG, ACCOUNTS, FLAGS
from dao import dao_base, account_dao
from entities import account


class GuiConfig:
    GUI_KEY = 'GUI_CONFIG'

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(UI_CONFIG)

    def __getitem__(self, item):
        return self._config[GuiConfig.GUI_KEY][item]


class GUIController(ui_controller.UIBase):
    def __init__(self):
        super().__init__()
        self._config = GuiConfig()

        window = self._window = tkinter.Tk()
        window.minsize(640, 480)
        window.title("Application")
        self._create_login_window()

    @staticmethod
    def render_function(func):
        def wrapped(self, *args, **kwargs):
            self._clear_window()
            func(self, *args, **kwargs)

        return wrapped

    def _clear_window(self):
        for widget in self._window.winfo_children():
            widget.destroy()

    @render_function
    def _create_login_window(self):
        borders = self._config['borders']

        root = tkinter.Frame(width=300, height=200, relief=tkinter.SOLID, borderwidth=borders, pady=15)
        root.pack_propagate(False)

        tkinter.Label(root, text='Login').pack()
        self._login = tkinter.Entry(root)
        self._login.pack()
        self._password = tkinter.Entry(root, show='*')
        self._password.pack()

        tkinter.Button(root, text='Login', command=self.process_login).pack()
        tkinter.Button(root, text='Register', command=self.process_register).pack()

        root.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

    def __show_admin_panel(self):
        window = self._window
        window.title('Admin panel')

        accounts = dao_base.DaoBase.create_from_data_source('accounts', account_dao.AccountDao)

        index = 0

        for dao in accounts.values():
            acc = account.Account()
            acc.from_dao(dao)

            tkinter.Label(window, text=acc.username).grid(row=index, column=0)
            tkinter.Label(window, text=ACCOUNTS.TO_STRING[acc.type]).grid(row=index, column=1)
            button = tkinter.Button(
                window,
                text=FLAGS.TO_BTN_LABEL[acc.flags]
            )

            button.config(
                command=partial(admin_panel.AdminPanel.toggle_ban, acc, button)
            )

            button.grid(row=index, column=3)
            index += 1

    def __show_customer_panel(self):
        pass

    def __show_worker_panel(self):
        pass

    @render_function
    def _create_account_interface(self, account):
        if not account:
            tkinter.messagebox.showerror('Error', 'Cannot render account window with NoneType')
            return
        if account.type == ACCOUNTS.ACCOUNT_ADMIN:
            self.__show_admin_panel()
        elif account.type == ACCOUNTS.ACCOUNT_CUSTOMER:
            self.__show_customer_panel()
        elif account.type == ACCOUNTS.ACCOUNT_WORKER:
            self.__show_worker_panel()
        else:
            tkinter.messagebox.showerror('Error', 'Invalid account type')

    @override
    def start(self) -> None:
        self._window.mainloop()

    @override
    def process_login(self):
        credentials = account_controller.Credentials(
            username=self._login.get(),
            password=self._password.get()
        )

        result, entity = account_controller.AccountController.try_login(credentials)

        if not entity:
            tkinter.messagebox.showerror('Login Error', f'Invalid Credentials: {result}')
            return

        if entity.flags == FLAGS.ACCOUNT_BLOCKED:
            tkinter.messagebox.showerror('Login Error', 'Your account is blocked')
            return

        self._create_account_interface(entity)

    @override
    def process_register(self):
        window = tkinter.Tk()
        window.title('Register')

        login = tkinter.Entry(window)
        login.pack(padx=10, pady=5)
        password = tkinter.Entry(window, show='*')
        password.pack()
        confirm = tkinter.Entry(window, show='*')
        confirm.pack(padx=10, pady=5)

        def try_register():
            if password.get() != confirm.get():
                tkinter.messagebox.showerror('Error', 'Passwords do not match')
                return

            credentials = account_controller.Credentials(
                login.get(),
                password.get()
            )
            result, entity = account_controller.AccountController.try_register(credentials)

            if not entity:
                tkinter.messagebox.showerror('Register Error', f'Invalid Credentials: {result}')
            window.destroy()

        tkinter.Button(window, text='Create account', command=try_register).pack(padx=10, pady=10)

        window.mainloop()

    @override
    def process_delete(self):
        pass

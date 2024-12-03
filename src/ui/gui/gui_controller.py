from __future__ import annotations

import tkinter.messagebox

import tkinter
import typing
import configparser
import tkcalendar
import datetime

from functools import partial

from ui import ui_controller
from ui.gui import admin_panel
from controllers import account_controller
from typing import override
from constants import UI_CONFIG, ACCOUNTS, FLAGS
from dao import dao_base, account_dao, customer_dao
from entities import account

from ui.gui.processor import account_processor, customer_processor, worker_processor


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

        self._account = None
        self._create_login_window()

    def _create_menu(self):
        change_creds = partial(account_processor.change_credentials_processor, self._account)
        show_info = partial(account_processor.show_account_info, self._account)

        show_msgs = partial(account_processor.show_messages, self._account)
        send_msg = partial(account_processor.create_message, self._account)

        window = self._window
        tkinter.Button(window, text='Change password', command=change_creds).pack()
        tkinter.Button(window, text='Show info', command=show_info).pack()
        tkinter.Button(window, text='Show messages', command=show_msgs).pack()
        tkinter.Button(window, text='Send message', command=send_msg).pack()


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

        root = tkinter.Frame(window)

        for dao in accounts.values():
            acc = account.Account(dao)

            tkinter.Label(root, text=acc.username).grid(row=index, column=0)
            tkinter.Label(root, text=ACCOUNTS.TO_STRING[acc.type]).grid(row=index, column=1)
            button = tkinter.Button(
                root,
                text=FLAGS.TO_BTN_LABEL[acc.flags]
            )

            button.config(
                command=partial(admin_panel.AdminPanel.toggle_ban, acc, button)
            )

            button.grid(row=index, column=3)
            index += 1

        root.pack()

    def __show_customer_panel(self):
        command = partial(customer_processor.create_user_data_view, self._account)
        create = partial(customer_processor.create_new_data, self._account)
        tkinter.Button(self._window, text='Show records', command=command).pack()
        tkinter.Button(self._window, text='New record', command=create).pack()

    def __show_worker_panel(self):
        tkinter.Button(self._window, text='Show records', command=worker_processor.create_all_customers_view).pack()

        entry = tkinter.Entry(self._window)
        entry.pack()

        def search():
            username = entry.get()

            worker_processor.show_customer(username)

        tkinter.Button(self._window, text='Search', command=search).pack()

        start = tkcalendar.DateEntry(self._window, selectmode='day', year=2021)
        stop = tkcalendar.DateEntry(self._window, selectmode='day', year=2025)

        start.pack()
        stop.pack()

        def filter_by_time():
            start_date = datetime.datetime.strptime(start.get(), '%m/%d/%y').timestamp()
            stop_date = datetime.datetime.strptime(stop.get(), '%m/%d/%y').timestamp()

            worker_processor.filter_by_data(start_date, stop_date)

        tkinter.Button(self._window, text='Filter', command=filter_by_time).pack()


    @render_function
    def _create_account_interface(self, account):
        if not account:
            tkinter.messagebox.showerror('Error', 'Cannot render account window with NoneType')
            return

        self._account = account
        self._create_menu()

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
        account_processor.process_register()

    @override
    def process_delete(self):
        pass

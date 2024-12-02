from __future__ import annotations

import typing
import tkinter

from controllers import account_controller
from entities import account

if typing.TYPE_CHECKING:
    from entities import account


def _create_credentials_form():
    window = tkinter.Tk()

    login = tkinter.Entry(window)
    login.pack(padx=10, pady=5)
    password = tkinter.Entry(window, show='*')
    password.pack()
    confirm = tkinter.Entry(window, show='*')
    confirm.pack(padx=10, pady=5)

    return window, login, password, confirm


def change_credentials_processor(acc: account.Account):
    window, login, password, new_password = _create_credentials_form()
    window.title('Change passowrd')

    def try_change_password():
        if login.get() != acc.username:
            tkinter.messagebox.showerror('Error', 'Username not yours')
            return

        if account.hash_password(password.get()) != acc.password:
            tkinter.messagebox.showerror('Error', 'Passwords do not match')
            return

        acc.password = new_password.get()
        window.destroy()

    tkinter.Button(window, text='Change password', command=try_change_password).pack(padx=10, pady=10)

    window.mainloop()


def process_register():
    window, login, password, confirm = _create_credentials_form()
    window.title('Register')

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


def show_account_info(acc: account.Account):
    window = tkinter.Tk()
    acc.create_widget(window)

    window.mainloop()

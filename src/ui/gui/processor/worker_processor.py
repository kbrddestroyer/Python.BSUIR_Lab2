from __future__ import annotations

import typing
import tkinter

from dao import dao_base, customer_dao, account_dao
from entities import customer
from constants import ACCOUNTS

if typing.TYPE_CHECKING:
    from typing import Dict


def generate_customers() -> Dict:
    all_customers = filter(lambda c: c.type == ACCOUNTS.ACCOUNT_CUSTOMER, dao_base.DaoBase.create_from_data_source(
        'accounts', account_dao.AccountDao
    ).values())

    customer_daos = dao_base.DaoBase.create_from_data_source(
        'customer_data', customer_dao.CustomerDao
    )

    customers_data = {}

    for c in all_customers:
        customers_data[c.username] = filter(lambda d: d.username == c.username, customer_daos.values())

    return customers_data


def create_all_customers_view():
    window = tkinter.Tk()
    window.title("All records")

    all_customers = generate_customers()

    for username, daos in all_customers.items():
        tkinter.Label(window, text=username).pack()
        for dao in daos:
            entity = customer.Customer(dao)
            entity.create_widget(window, False)

    window.mainloop()


def show_customer(username: str):
    window = tkinter.Tk()
    window.title("All records")
    all_customers = generate_customers()

    data = all_customers.get(username, [])
    for dao in data:
        entity = customer.Customer(dao)
        entity.create_widget(window, False)

    window.mainloop()


def filter_by_data(start: float, stop: float, username: str = None):
    window = tkinter.Tk()
    window.title("All records")
    all_customers = generate_customers()

    def show_customer(name):
        l_data = all_customers.get(name, [])

        tkinter.Label(window, text=name).pack()
        for dao in l_data:
            if not start <= dao.timestamp <= stop:
                continue

            entity = customer.Customer(dao)
            entity.create_widget(window, False)

    if not username:
        for username in all_customers.keys():
            show_customer(username)
        return
    show_customer(username)

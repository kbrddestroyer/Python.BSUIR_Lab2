from __future__ import annotations

import typing
import tkinter

from tkinter import ttk

from dao import dao_base, customer_dao
from entities import customer

if typing.TYPE_CHECKING:
    from entities import account
    from typing import Dict


def create_new_data(acc: account.Account):
    dao = customer_dao.CustomerDao({
        'username': acc.username,
        'unique_id': customer.Customer.generate_id(),
        'timestamp': customer.Customer.generate_timestamp()
    })
    customer_entity = customer.Customer(dao)

    window = tkinter.Tk()
    window.title('Customer records')

    customer_entity.create_widget(window)
    customer_entity.destroy()

    window.mainloop()


def create_user_data_view(acc: account.Account):
    all_records : Dict[dao_base.DaoBase] = dao_base.DaoBase.create_from_data_source(
        'customer_data', customer_dao.CustomerDao
    )
    if not all_records:
        return

    window = tkinter.Tk()
    window.title('Customer records')

    username = acc.username

    for record in all_records.values():
        if record.username == username:
            customer_entity = customer.Customer(record)
            customer_entity.create_widget(window, False)
            ttk.Separator(window).pack()
            customer_entity.destroy()

    window.mainloop()

from __future__ import annotations

import typing
import tkinter

from dao import dao_base, customer_dao
from entities import customer


def create_all_customers_view():
    window = tkinter.Tk()
    window.title("All records")

    daos = dao_base.DaoBase.create_from_data_source(
        'customer_data', customer_dao.CustomerDao
    )

    for dao in daos.values():
        tkinter.Label(window, text=dao.username).pack()
        entity = customer.Customer(dao)
        entity.create_widget(window, False)

    window.mainloop()

from __future__ import annotations

import typing
import tkinter

if typing.TYPE_CHECKING:
    from dao import dao_base


class DaoWidget(tkinter.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_dao(self, dao: dao_base.DaoBase, blacklist=None, show_btn = True) -> None:
        if blacklist is None:
            blacklist = []
        data = {}

        for k, v in dao.__dict__().items():
            if k in blacklist:
                continue

            data[k] = entry = tkinter.Entry(self)
            entry.pack()
            entry.insert(0, v)

        if not show_btn:
            return

        def apply():
            for k, v in data.items():
                dao[k] = v.get()
            dao.apply()
            self.destroy()

        tkinter.Button(self, text='Apply', command=apply).pack()

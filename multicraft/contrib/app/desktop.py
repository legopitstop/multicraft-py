__all__ = ["MulticraftDesktop"]

from tkinter import (
    Tk,
    Event,
    Label,
    Listbox,
    Frame,
    StringVar,
)
from tkinter.font import Font
import logging

from multicraft import Host, MulticraftAPI

from .view import __views__, View


class MulticraftDesktop(Tk, MulticraftAPI):
    def __init__(self, host: Host, user: str, server_id: int, key: str = ""):
        Tk.__init__(self)
        self.api = MulticraftAPI(host, user, key, logging.getLogger("MulticraftAPI"))
        self.api.server_id = server_id

        self.title("multicraft")
        self.geometry("700x600")
        self.minsize(700, 500)

        self.views: list[View] = []
        self.body()

    def body(self):
        # Widgets
        self.title = StringVar(value="Test")

        self.title_lbl = Label(
            self, textvariable=self.title, font=Font(size=15, weight="bold"), anchor="w"
        )

        self.navbar = Listbox(self)
        self.navbar.bind("<<ListboxSelect>>", self._listbox_select)

        self.title_lbl.grid(row=0, column=1, sticky="ew")
        self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # Responsive
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # TODO
        # Add "quick console" that sticks to the bottom right
        # [status]
        # text
        # [type a command...] [start] [stop] [restart]

        # Bindings
        self.bind("<F5>", lambda e: self.refresh())

    def refresh(self):
        for view in self.views:
            view.refresh()

    def _listbox_select(self, e: Event) -> None:
        cur = self.navbar.curselection()
        if len(cur) == 0:
            return
        self.show_view(cur[0])

    def add_view(self, view: View):
        obj = view(self, self.api)
        frame = Frame(self)
        obj._frame = frame
        obj.body(frame)
        self.navbar.insert("end", obj.get_name())
        self.views.append(obj)

    def show_view(self, view_id: str | int) -> None:
        if view_id == "login":
            self.navbar.grid_forget()
        else:
            self.navbar.grid(row=0, column=0, rowspan=2, sticky="ns")

        for i, view in enumerate(self.views):
            view.hide()
            if view.get_id() == view_id or i == view_id:
                self.title.set(view.get_name())
                view.show()
        return None

    def mainloop(self) -> None:
        for view in __views__:
            self.add_view(view)
        self.show_view("login")
        super().mainloop()

    def destroy(self):
        super().destroy()

__all__ = ['__views__','view', 'View']

from tkinter import messagebox, StringVar, Label, Entry, Button, Text
from tkinter.font import Font
from tkinter.ttk import Treeview
from typing import List
import os

class View:
    ID = "unknown"
    NAME = "Unknown"

    def __init__(self, parent, api):
        self.parent = parent
        self.api = api

    def body(self, frame) -> None:
        raise NotImplementedError()

    def refresh(self) -> None: ...

    def get_id(self) -> str:
        return self.ID

    def get_name(self) -> str:
        return self.NAME

    def hide(self) -> None:
        self._frame.grid_forget()

    def show(self) -> None:
        self._frame.grid(row=1, column=1, sticky="nesw", padx=5)


__views__: List[View] = []

# TODO: LOGIN UI


def view(cls) -> View:
    def wrapper():
        global __views__
        __views__.append(cls)
        return cls

    return wrapper()


@view
class LoginPage(View):
    ID = "login"
    NAME = "Login"

    def body(self, frame):
        self.USERNAME_VAR = StringVar(value=os.getenv("MULTICRAFT_USER"))
        self.PASSWORD_VAR = StringVar(value=os.getenv("MULTICRAFT_PASSWORD"))

        self.username_lbl = Label(
            frame, text="Username", font=Font(size=12), anchor="w"
        )
        self.username_entry = Entry(frame, textvariable=self.USERNAME_VAR)

        self.password_lbl = Label(
            frame, text="Password", font=Font(size=12), anchor="w"
        )
        self.password_entry = Entry(frame, textvariable=self.PASSWORD_VAR, show="*")

        self.submit_btn = Button(frame, text="Login", command=self.submit)

        self.username_lbl.grid(row=0, column=0, sticky="ew")
        self.username_entry.grid(row=1, column=0, sticky="ew")
        self.password_lbl.grid(row=2, column=0, sticky="ew")
        self.password_entry.grid(row=3, column=0, sticky="ew")
        self.submit_btn.grid(row=4, column=0, sticky="e")

    def submit(self):
        print(self.parent.title)
        messagebox.showwarning("", "MESSAGE", master=self.parent)


@view
class HomeView(View):
    ID = "home"
    NAME = "Home"

    def body(self, frame):
        self.STATUS_VAR = StringVar(value="Offline")
        self.NAME_VAR = StringVar(value="My Server")
        self.IP_VAR = StringVar(value="xx.xxx.xxx.xxx:xxxx")
        self.SUBDOMAIN_VAR = StringVar(value="xxx")

        self.status_lbl = Label(frame, text="Status", font=Font(size=12), anchor="w")
        self.status_entry = Label(
            frame, textvariable=self.STATUS_VAR, fg="red", anchor="w"
        )
        self.name_lbl = Label(frame, text="Name", font=Font(size=12), anchor="w")
        self.name_entry = Entry(frame, textvariable=self.NAME_VAR)
        self.ip_lbl = Label(frame, text="IP Address", font=Font(size=12), anchor="w")
        self.ip_entry = Label(frame, textvariable=self.IP_VAR, anchor="w")
        self.subdomain_lbl = Label(
            frame, text="Subdomain", font=Font(size=12), anchor="w"
        )
        self.subdomain_entry = Label(frame, textvariable=self.SUBDOMAIN_VAR, anchor="w")

        self.status_lbl.grid(row=0, column=0, sticky="ew")
        self.status_entry.grid(row=1, column=0, sticky="ew")
        self.name_lbl.grid(row=2, column=0, sticky="ew")
        self.name_entry.grid(row=3, column=0, sticky="ew")
        self.ip_lbl.grid(row=4, column=0, sticky="ew")
        self.ip_entry.grid(row=5, column=0, sticky="ew")
        self.subdomain_lbl.grid(row=6, column=0, sticky="ew")
        self.subdomain_entry.grid(row=7, column=0, sticky="ew")
        self.refresh()

    def refresh(self): ...


@view
class ConsoleView(View):
    ID = "console"
    NAME = "Console"

    def body(self, frame):
        self.COMMAND = StringVar()

        self.text = Text(frame, state="disabled")
        self.send_cmd = Entry(frame, textvariable=self.COMMAND)
        self.send_cmd.bind("<Return>", self.send_command)
        self.start_btn = Button(frame, text="Start")
        self.stop_btn = Button(frame, text="Stop")
        self.restart_btn = Button(frame, text="Restart")

        self.text.grid(row=0, column=0, columnspan=4, sticky="nesw")
        self.send_cmd.grid(row=1, column=0, sticky="nesw")
        self.start_btn.grid(row=1, column=1, sticky="nesw")
        self.stop_btn.grid(row=1, column=2, sticky="nesw")
        self.restart_btn.grid(row=1, column=3, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def send_command(self, e) -> None:
        self.text.configure(state="normal")
        cmd = self.COMMAND.get()
        match cmd:
            case "clear":
                self.text.delete(0.0, "end")
                return
            case _:
                self.text.insert("end", cmd + "\n")
        self.COMMAND.set("")
        self.text.configure(state="disabled")

    def refresh(self):
        self.text.configure(state="normal")
        self.text.delete(0.0, "end")
        self.text.insert(
            "end", "[00:00:00] [Server thread/INFO]: Done (4.969s)! Run /help for help!"
        )
        self.text.configure(state="disabled")


@view
class FilesView(View):
    ID = "files"
    NAME = "Files"

    def body(self, frame):
        self.tree = Treeview(frame)
        self.tree["columns"] = ("#1", "#2", "#3")
        self.tree.column("#0", width=20)
        self.tree.column("#1", width=10, anchor="center")
        self.tree.column("#2", width=10, anchor="center")
        self.tree.column("#3", width=3, anchor="center")

        self.tree.heading("#0", text="Name")
        self.tree.heading("#1", text="Date Modified")
        self.tree.heading("#2", text="Type")
        self.tree.heading("#3", text="Size")
        self.tree.grid(row=0, column=0, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(10):
            self.tree.insert(
                "",
                "end",
                i,
                text=f"Example {i}.txt",
                value=("Aug, 8, 2024, 12:00", "Text File", "1 KB"),
            )


@view
class DatabaseView(View):
    ID = "databases"
    NAME = "Databases"

    def body(self, frame):
        self.none(frame)

    def none(self, frame):
        self.none_lbl = Label(frame, text="It looks like you have no databases.")
        self.none_btn = Button(frame, text="Create Database", state="disabled")
        self.none_lbl.grid(row=0, column=0)
        self.none_btn.grid(row=1, column=0)

        frame.grid_columnconfigure(0, weight=1)

    def refresh(self): ...


@view
class BackupsView(View):
    ID = "backups"
    NAME = "Backups"

    def body(self, frame):
        self.tree = Treeview(frame)
        self.tree["columns"] = "#1"
        self.tree.column("#0", width=10)
        self.tree.column("#1", width=10, anchor="center")

        self.tree.heading("#0", text="Backup Name")
        self.tree.heading("#1", text="Date Created")
        self.tree.grid(row=0, column=0, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(10):
            self.tree.insert(
                "",
                "end",
                i,
                text=f"Example {i}",
                value=("Aug, 8, 2024, 12:00"),
            )


@view
class PlayersView(View):
    ID = "players"
    NAME = "Players"

    def body(self, frame):
        self.tree = Treeview(frame)
        self.tree["columns"] = ("#1", "#2", "#3")
        self.tree.column("#0", width=10)
        self.tree.column("#1", width=10, anchor="center")
        self.tree.column("#2", width=10, anchor="center")
        self.tree.column("#3", width=10, anchor="center")

        self.tree.heading("#0", text="Username")
        self.tree.heading("#1", text="Last Seen")
        self.tree.heading("#2", text="IP Address")
        self.tree.heading("#3", text="Actions")
        self.tree.grid(row=0, column=0, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(10):
            self.tree.insert(
                "",
                "end",
                i,
                text=f"Steve {i}",
                value=("Aug, 8, 2024, 12:00", "xxx.xxx.xxx.xxx", "DELETE"),
            )


@view
class SchedulesView(View):
    ID = "schedules"
    NAME = "Schedules"

    def body(self, frame):
        self.tree = Treeview(frame)
        self.tree["columns"] = ("#1", "#2")
        self.tree.column("#0", width=10)
        self.tree.column("#1", width=10, anchor="center")
        self.tree.column("#2", width=10, anchor="center")

        self.tree.heading("#0", text="Name")
        self.tree.heading("#1", text="Status")
        self.tree.heading("#2", text="Last run")
        self.tree.grid(row=0, column=0, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(10):
            self.tree.insert(
                "",
                "end",
                i,
                text=f"Server Restart {i}",
                value=("Active", "Aug, 8, 2024, 12:00"),
            )


@view
class UsersView(View):
    ID = "users"
    NAME = "Users"

    def body(self, frame):
        self.tree = Treeview(frame)
        self.tree["columns"] = "#1"
        self.tree.column("#0", width=10)
        self.tree.column("#1", width=10, anchor="center")

        self.tree.heading("#0", text="Username")
        self.tree.heading("#1", text="Permission Level")
        self.tree.grid(row=0, column=0, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(10):
            self.tree.insert(
                "",
                "end",
                i,
                text=f"Steve {i}",
                value=("1"),
            )


@view
class ChatView(View):
    ID = "chat"
    NAME = "Chat"

    def body(self, frame):
        self.MESSAGE = StringVar()

        self.text = Text(frame, state="disabled")
        self.send_msg = Entry(frame, textvariable=self.MESSAGE)
        self.send_msg.bind("<Return>", self.send_message)
        self.start_btn = Button(frame, text="Send", command=self.send_message)

        self.text.grid(row=0, column=0, columnspan=2, sticky="nesw")
        self.send_msg.grid(row=1, column=0, sticky="nesw")
        self.start_btn.grid(row=1, column=1, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def refresh(self):
        self.text.configure(state="normal")
        self.text.delete(0.0, "end")
        self.text.insert("end", "[Notch] Hello World")
        self.text.configure(state="disabled")

    def send_message(self, e=None) -> None:
        self.text.configure(state="normal")
        cmd = self.MESSAGE.get()
        self.text.insert("end", cmd + "\n")
        self.MESSAGE.set("")
        self.text.configure(state="disabled")


@view
class CommandsView(View):
    ID = "commands"
    NAME = "Commands"

    def body(self, frame):
        self.tree = Treeview(frame)
        self.tree["columns"] = ("#1", "#2", "#3")
        self.tree.column("#0", width=10)
        self.tree.column("#1", width=10, anchor="center")
        self.tree.column("#2", width=10, anchor="center")
        self.tree.column("#3", width=10, anchor="center")

        self.tree.heading("#0", text="Name")
        self.tree.heading("#1", text="Level")
        self.tree.heading("#2", text="Response")
        self.tree.heading("#3", text="Role")
        self.tree.grid(row=0, column=0, sticky="nesw")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in range(10):
            self.tree.insert(
                "",
                "end",
                i,
                text=f"Command {i}",
                value=("5", "404", "owner"),
            )


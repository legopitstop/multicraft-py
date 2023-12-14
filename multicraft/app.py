"""
A bear boned multicraft client UI
"""
from tkinter import Tk, Event, Label, Listbox, Frame, Button

from . import MulticraftAPI

__all__ = ['MulticraftApp']

pages = []

def page(cls):
    def wrapper():
        global pages
        pages.append(cls)
    return wrapper()

class Page:
    def __init__(self, frame, api:MulticraftAPI, name):
        self.frame = frame
        self.api = api
        self.name = name
        
        frm = Frame(frame)
        self._nav_lbl = Label(frm, text='Servers > legopitstop\'s Minecraft Server')
        self._nav_lbl.grid(row=0, column=0, sticky='nwe')
        frm.grid(row=0, column=0, sticky='ew')

@page
class HomePage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Home')
        self._status_lbl = Label(frame, text='P')
        self._start_btn = Button(frame, text='Start', command=lambda s=self.api.server: self.api.start_server(s))
        self._stop_btn = Button(frame, text='Stop', command=lambda s=self.api.server: self.api.stop_server(s))
        self._restart_btn = Button(frame, text='Restart', command=lambda s=self.api.server: self.api.restart_server(s))
        self._kill_btn = Button(frame, text='Kill', command=lambda s=self.api.server: self.api.kill_server(s))

        self._status_lbl.grid(row=1, column=0)
        self._start_btn.grid(row=1, column=1)
        self._stop_btn.grid(row=1, column=2)
        self._restart_btn.grid(row=1, column=3)
        self._kill_btn.grid(row=1, column=4)

@page
class ConsolePage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Console')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class ChatPage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Chat')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class PlayersPage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Players')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class BackupManagerPage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Backup Manager')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class CommandsPage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Commands')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class ScheduledTasksPage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Scheduled Tasks')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class UsersPage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'Users')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

@page
class DatabasePage(Page):
    def __init__(self, frame, api):
        super().__init__(frame, api, 'MySQL Database')
        Label(frame, text=self.name).grid(row=0, column=0, sticky='nw')

# App
class MulticraftApp(Tk, MulticraftAPI):
    def __init__(self, url:str, user:str, server:int, key:str=None):
        Tk.__init__(self)
        self.api  = MulticraftAPI(url, user, key)
        self.api.server = server
        self.title('multicraft')
        self.geometry('700x600')

        self.pages = []

        # Widgets
        self._pages = Listbox(self)
        self._pages.grid(row=0, column=0, sticky='nsw')
        self._pages.bind('<<ListboxSelect>>', self._listbox_select)

        # Responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _listbox_select(self, e:Event):
        cur = self._pages.curselection()
        if len(cur) == 0: return
        self.page(cur[0])

    def page(self, page_id:int):
        for page in self.pages: page.frame.forget()
        p = self.pages[page_id]
        p.frame.grid(row=0, column=1, sticky='nesw')

    def mainloop(self):
        global pages
        for p in pages:
            frame = Frame(self)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            page = p(frame, self.api)
            self._pages.insert('end', page.name)
            self.pages.append(page)
        self.page(0)
        super().mainloop()



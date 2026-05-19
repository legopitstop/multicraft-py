__all__ = [
    "Host",
    "Status",
    "ScheduleStatus",
    "Role",
    "Mode",
    "BackupStatus",
    "User",
    "Server",
    "Command",
    "ServerStatus",
    "ChatMessage",
    "Player",
    "ServerResources",
    "Schedule",
    "Database",
    "Backup",
]

from typing import Self
from enum import Enum
from pydantic import BaseModel
import datetime


class Status(Enum):
    online = "online"
    offline = "offline"


class ScheduleStatus(Enum):
    scheduled = 0
    rescheduled = 1
    done = 2
    paused = 3

    @classmethod
    def from_int(self, value):
        match value:
            case 0:
                return ScheduleStatus.scheduled
            case 1:
                return ScheduleStatus.rescheduled
            case 2:
                return ScheduleStatus.done
            case 3:
                return ScheduleStatus.paused
            case _:
                return ScheduleStatus.scheduled


class Role(Enum):
    none = "none"
    user = "user"
    guest = "guest"
    mod = "mod"
    smod = "smod"
    admin = "admin"
    coowner = "coowner"
    owner = "owner"

    @classmethod
    def from_int(cls, value: int):
        match value:
            case 0:
                return Role.none
            case 20:
                return Role.user
            case 10:
                return Role.guest
            case 30:
                return Role.mod
            case 35:
                return Role.smod
            case 40:
                return Role.admin
            case 45:
                return Role.coowner
            case 50:
                return Role.owner
            case _:
                return Role.none

    def to_int(self) -> int:
        match self._value_:
            case "none":
                return 0
            case "user":
                return 20
            case "guest":
                return 10
            case "mod":
                return 30
            case "smod":
                return 35
            case "admin":
                return 40
            case "coowner":
                return 45
            case "owner":
                return 50
            case _:
                return 0


class Mode(Enum):
    ro = "ro"
    rw = "rw"


class BackupStatus(Enum):
    done = "done"


class Host(BaseModel):
    homepage: str
    api_url: str
    sftp_host: str
    sftp_port: int = 22


class User(BaseModel):
    id: int
    name: str
    email: str
    global_role: str
    lang: str
    theme: str
    gauth_secret: str
    gauth_token: str
    timezone: str


class Server(BaseModel):
    id: int
    name: str
    daemon_id: int = 0
    ip: str = ""
    port: int = 0
    players: int = 0
    memory: int = 0

    def start(self) -> Self:
        self._api.start_server(self.id)
        return self

    def stop(self) -> Self:
        self._api.stop_server(self.id)
        return self

    def restart(self) -> Self:
        self._api.restart_server(self.id)
        return self

    def kill(self) -> Self:
        self._api.kill_server(self.id)
        return self


class Command(BaseModel):
    id: int
    name: str
    server_id: int = 0
    level: int = 0
    prereq: int = 0
    chat: str = ""
    response: str = ""
    run: str = ""
    hidden: bool = False
    role: Role = Role.none

    def __call__(self):
        raise NotImplementedError()

    def delete(self) -> Self:
        self._api.delete_server(self.id)
        return self


class ServerStatus(BaseModel):
    status: Status
    online_players: int
    max_players: int
    players: list[str] = []

    def is_online(self) -> bool:
        return self.status == Status.online

    def is_offline(self) -> bool:
        return self.status == Status.offline


class ServerResources(BaseModel):
    cpu: float
    memory: float
    quota: int


class ChatMessage(BaseModel):
    text: str
    name: str
    time: datetime.datetime


class Player(BaseModel):
    id: int
    name: str
    server_id: int = 0
    level: int = 0
    lastseen: datetime.datetime = datetime.datetime.now()
    banned: bool = False
    op: bool = False
    status: Status = Status.offline
    ip: str = ""
    previps: str = ""
    quitreason: str = ""

    def delete(self) -> Self:
        self._api.delete_player(self.id)
        return self


class Schedule(BaseModel):
    id: int
    name: str
    server_id: int = 0
    scheduled_ts: datetime.datetime = datetime.datetime.now()  # ts
    last_run_ts: datetime.datetime = datetime.datetime.now()
    interval: float = 0.0
    command: int = 0  # cmd
    run_for: int = 0
    status: int = 0
    args: str = ""
    hidden: bool = False

    def delete(self) -> Self:
        self._api.delete_schedule(self.id)
        return self


class Database(BaseModel):
    host: str
    name: str
    username: str
    password: str
    link: str

    def delete(self) -> Self:
        self._api.delete_database(self.id)
        return self


class Backup(BaseModel):
    status: BackupStatus
    ftp: str
    message: str
    file: str
    time: datetime.datetime

from enum import Enum
import datetime

__all__ = ['Status','ScheduleStatus','Role','Mode','BackupStatus','User','Server','Command','ServerStatus','ChatMessage','Player','ServerResources','Schedule','Database','Backup']

class Status(Enum):
    online = 'online'
    offline = 'offline'

class ScheduleStatus(Enum):
    scheduled = 0
    rescheduled = 1
    done = 2
    paused = 3

    @classmethod
    def from_int(self, value):
        match value:
            case 0: return ScheduleStatus.scheduled
            case 1: return ScheduleStatus.rescheduled
            case 2: return ScheduleStatus.done
            case 3: return ScheduleStatus.paused
            case _: return ScheduleStatus.scheduled

class Role(Enum):
    none = 'none'
    user = 'user'
    guest = 'guest'
    mod = 'mod'
    smod = 'smod'
    admin = 'admin'
    coowner = 'coowner'
    owner = 'owner'

    @classmethod
    def from_int(cls, value:int):
        match value:
            case 0: return Role.none
            case 20: return Role.user
            case 10: return Role.guest
            case 30: return Role.mod
            case 35: return Role.smod
            case 40: return Role.admin
            case 45: return Role.coowner
            case 50: return Role.owner
            case _: return Role.none

    def to_int(self) -> int:
        match self._value_:
            case 'none': return 0
            case 'user': return 20
            case 'guest': return 10
            case 'mod': return 30
            case 'smod': return 35
            case 'admin': return 40
            case 'coowner': return 45
            case 'owner': return 50
            case _: return 0

class Mode(Enum):
    ro = 'ro'
    rw = 'rw'

class BackupStatus(Enum):
    done = 'done'

class User:
    def __init__(self, id:int, name:str, email:str, global_role: str, lang:str, theme:str, gauth_secret:str, gauth_token:str, timezone:str):
        self.id = id
        self.name = name
        self.email = email
        self.global_role = global_role
        self.lang = lang
        self.theme = theme
        self.gauth_secret = gauth_secret
        self.gauth_token = gauth_token
        self.timezone = timezone

    def __repr__(self):
        return f"Server(id={self.id}, name='{self.name}')"

    def __str__(self) -> str:
        return f"Server(id={self.id}, name='{self.name}', email='{self.email}')"
    
    @property
    def id(self) -> int:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:int):
        if isinstance(value, str):
            self.id = int(value)
        elif isinstance(value, int):
            setattr(self, '_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def email(self) -> str:
        return getattr(self, '_email')
    
    @email.setter
    def email(self, value:str):
        setattr(self, '_email', str(value))
        
    @property
    def global_role(self) -> str:
        return getattr(self, '_global_role')
    
    @global_role.setter
    def global_role(self, value:str):
        setattr(self, '_global_role', str(value))
        
    @property
    def lang(self) -> str:
        return getattr(self, '_lang')
    
    @lang.setter
    def lang(self, value:str):
        setattr(self, '_lang', str(value))
        
    @property
    def theme(self) -> str:
        return getattr(self, '_theme')
    
    @theme.setter
    def theme(self, value:str):
        setattr(self, '_theme', str(value))
    
    @property
    def gauth_secret(self) -> str:
        return getattr(self, '_gauth_secret')
    
    @gauth_secret.setter
    def gauth_secret(self, value:str):
        setattr(self, '_gauth_secret', str(value))

    @property
    def gauth_token(self) -> str:
        return getattr(self, '_gauth_token')
    
    @gauth_token.setter
    def gauth_token(self, value:str):
        setattr(self, '_gauth_token', str(value))

    @property
    def timezone(self) -> str:
        return getattr(self, '_timezone')
    
    @timezone.setter
    def timezone(self, value:str):
        setattr(self, '_timezone', str(value))

    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        self.id = data.pop('id')
        if 'name' in data: self.name = data.pop('name')
        if 'email' in data: self.email = data.pop('email')
        if 'global_role' in data: self.global_role = data.pop('global_role')
        if 'lang' in data: self.lang = data.pop('lang')
        if 'theme' in data: self.theme = data.pop('theme')
        if 'gauth_secret' in data: self.gauth_secret = data.pop('gauth_secret')
        if 'gauth_token' in data: self.gauth_token = data.pop('gauth_token')
        if 'timezone' in data: self.timezone = data.pop('timezone')
        return self

class Server:
    def __init__(self, id:int, name:str, daemon_id:int=None, ip:str=None, port:int=None, players:int=None, memory:int=None):
        self.id = id
        self.name = name
        self.daemon_id = daemon_id
        self.ip = ip
        self.port = port
        self.players = players
        self.memory = memory

    def __repr__(self):
        return f"Server(id={self.id}, name='{self.name}')"

    def __str__(self) -> str:
        return f"Server(id={self.id}, name='{self.name}', daemon_id={self.daemon_id}, ip='{self.ip}', port={self.port})"
    
    @property
    def id(self) -> int:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:str):
        if isinstance(value, str):
            self.id = int(value)
        elif isinstance(value, int):
            setattr(self, '_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def daemon_id(self) -> str:
        return getattr(self, '_daemon_id')
    
    @daemon_id.setter
    def daemon_id(self, value:str):
        setattr(self, '_daemon_id', str(value))

    @property
    def ip(self) -> str:
        return getattr(self, '_ip')
    
    @ip.setter
    def ip(self, value:str):
        setattr(self, '_ip', str(value))

    @property
    def port(self) -> int:
        return getattr(self, '_port', 25565)
    
    @port.setter
    def port(self, value:int):
        if value is None: self.port = 25565
        elif isinstance(value, str):
            self.port = int(value)
        elif isinstance(value, int):
            setattr(self, '_port', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def players(self) -> int:
        return getattr(self, '_players', 0)
    
    @players.setter
    def players(self, value:int):
        if value is None: self.players = 0
        elif isinstance(value, str):
            self.players = int(value)
        elif isinstance(value, int):
            setattr(self, '_players', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def memory(self) -> int:
        return getattr(self, '_memory', 0)
    
    @memory.setter
    def memory(self, value:int):
        if value is None: self.memory = 0
        elif isinstance(value, str):
            self.memory = int(value)
        elif isinstance(value, int):
            setattr(self, '_memory', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    def start(self):
        raise NotImplementedError()
    
    def stop(self):
        raise NotImplementedError()
    
    def restart(self):
        raise NotImplementedError()
    
    def kill(self):
        raise NotImplementedError()
    
    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        if 'id' in data: self.id = data.pop('id')
        if 'name' in data: self.name = data.pop('name')
        if 'daemon_id' in data: self.daemon_id = data.pop('daemon_id')
        if 'ip' in data: self.ip = data.pop('ip')
        if 'port' in data: self.port = data.pop('port')
        if 'players' in data: self.players = data.pop('players')
        if 'memory' in data: self.memory = data.pop('memory')
        return self

class Command:
    def __init__(self, id:int, name:str, server_id:int=None, level:int=None, prereq:int=0, chat:str=None, response:str=None, run:str=None, hidden:bool=None, role:Role=None):
        self.id = id
        self.name = name
        self.server_id = server_id
        self.level = level
        self.prereq = prereq
        self.chat = chat
        self.response = response
        self.run = run
        self.hidden = hidden

        if role is not None:
            self.level = Role[role].to_int()

    def __repr__(self):
        return f"Command(id={self.id}, name='{self.name}')"
    
    def __str__(self) -> str:
        return f"Command(id={self.id}, name='{self.name}', server_id={self.server_id}, level={self.level}, prereq={self.prereq}, hidden={self.hidden})"
    
    @property
    def id(self) -> int:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:int):
        if isinstance(value, str):
            self.id = int(value)
        elif isinstance(value, int):
            setattr(self, '_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def server_id(self) -> int:
        return getattr(self, '_server_id', 0)
    
    @server_id.setter
    def server_id(self, value:int):
        if isinstance(value, str):
            self.server_id = int(value)
        elif isinstance(value, int):
            setattr(self, '_server_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def level(self) -> int:
        return getattr(self, '_level', 0)
    
    @property
    def role(self) -> Role:
        return Role.from_int(self.level)
    
    @level.setter
    def level(self, value:int):
        if value is None: self.level = 0
        elif isinstance(value, str):
            self.level = int(value)
        elif isinstance(value, int):
            setattr(self, '_level', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def prereq(self) -> int:
        return getattr(self, '_prereq', 0)
    
    @prereq.setter
    def prereq(self, value:int):
        if isinstance(value, str):
            self.prereq = int(value)
        elif isinstance(value, int):
            setattr(self, '_prereq', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def chat(self) -> str:
        return getattr(self, '_chat', None)
    
    @chat.setter
    def chat(self, value:str):
        setattr(self, '_chat', str(value))
        
    @property
    def response(self) -> str:
        return getattr(self, '_response', None)
    
    @response.setter
    def response(self, value:str):
        setattr(self, '_response', str(value))

    @property
    def run(self) -> str:
        return getattr(self, '_run', None)
    
    @run.setter
    def run(self, value:str):
        setattr(self, '_run', str(value))

    @property
    def hidden(self) -> bool:
        return getattr(self, '_hidden', False)
    
    @hidden.setter
    def hidden(self, value:bool):
        if value is None: self.hidden = False
        elif isinstance(value, str):
            self.hidden = True if value == '1' else False
        elif isinstance(value, bool):
            setattr(self, '_hidden', value)
        else:
            raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")

    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        self.id = data.pop('id')
        self.name = data.pop('name')
        if 'server_id' in data: self.server_id = data.pop('server_id')
        if 'level' in data: self.level = data.pop('level')
        if 'role' in data: self.level = Role[data.pop('role')].to_int()
        if 'prereq' in data: self.prereq = data.pop('prereq')
        if 'chat' in data: self.chat = data.pop('chat')
        if 'response' in data: self.response = data.pop('response')
        if 'run' in data: self.run = data.pop('run')
        if 'hidden' in data: self.hidden = data.pop('hidden')
        return self
    
    def delete(self):
        raise NotImplementedError()
    
    def run(self):
        raise NotImplementedError()
    
class ServerStatus:
    def __init__(self, status:Status, online_players:int, max_players:int, players:list=[]):
        self.status = status
        self.online_players = online_players
        self.max_players = max_players
        self.players = players

    def __repr__(self):
        return f"ServerStatus(status={self.status}, online_players={self.online_players}, max_players={self.max_players})"
    
    def __str__(self) -> str:
        return f"ServerStatus(status={self.status}, online_players={self.online_players}, max_players={self.max_players})"
    
    @property
    def status(self) -> Status:
        return getattr(self, '_status')
    
    @status.setter
    def status(self, value:Status):
        if isinstance(value, str):
            self.status = Status[str(value)]
        elif isinstance(value, Status):
            setattr(self, '_status', value)
        else:
            raise TypeError(f"Expected Status but got '{value.__class__.__name__}' instead")

    @property
    def online_players(self) -> int:
        return getattr(self, '_online_players')
    
    @online_players.setter
    def online_players(self, value:int):
        if value is None: self.online_players = 0
        elif isinstance(value, str):
            self.online_players = int(value)
        elif isinstance(value, int):
            setattr(self, '_online_players', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
    
    @property
    def max_players(self) -> int:
        return getattr(self, '_max_players')
    
    @max_players.setter
    def max_players(self, value:int):
        if value is None: self.max_players = 0
        elif isinstance(value, str):
            self.max_players = int(value)
        elif isinstance(value, int):
            setattr(self, '_max_players', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
    
    @property
    def players(self) -> list[str]:
        return getattr(self, '_players')

    @players.setter
    def players(self, value:list):
        if value is None: self.players = []
        elif isinstance(value, list):
            setattr(self, '_players', [str(x) for x in value])
        else:
            raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
    
    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        if 'status' in data: self.status = data.pop('status')
        if 'onlinePlayers' in data: self.online_players = data.pop('onlinePlayers')
        if 'maxPlayers' in data: self.max_players = data.pop('maxPlayers')
        if 'players' in data: self.players = data.pop('players')
        return self
    
class ChatMessage:
    def __init__(self, text:str, name:str, time:datetime):
        self.text = text
        self.name = name
        self.time = time

    def __repr__(self):
        return f"ChatMessage(text='{self.text}', name='{self.name}')"
    
    def __str__(self) -> str:
        return f"ChatMessage(text='{self.text}', name='{self.name}', time='{self.time}')"
    
    @property
    def text(self) -> str:
        return getattr(self, '_text')
    
    @text.setter
    def text(self, value:str):
        setattr(self, '_text', str(value))
    
    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))
    
    @property
    def time(self) -> datetime:
        return getattr(self, '_time')
    
    @time.setter
    def time(self, value:datetime.datetime|float|int):
        if isinstance(value, (float,int)):
            self.time = datetime.datetime.fromtimestamp(value)
        elif isinstance(value, datetime.datetime):
            setattr(self, '_time', value)
        elif isinstance(value, str):
            self.time = float(value)
        else:
            raise TypeError(f"Expected datetime but got '{value.__class__.__name__}' instead")
    
    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        if 'text' in data: self.text = data.pop('text')
        if 'name' in data: self.name = data.pop('name')
        if 'time' in data: self.time = data.pop('time')
        return self

class Player:
    def __init__(self, id:int, name:str, server_id:int=None, level:int=0, lastseen:datetime.datetime=None, banned:bool=None, op:bool=None, status: Status=Status.offline, ip:str=None, previps:str=None, quitreason:str=None):
        self.id = id
        self.name = name
        self.server_id = server_id
        self.level = level
        self.lastseen = lastseen
        self.banned = banned
        self.op = op
        self.status = status
        self.ip = ip
        self.previps = previps
        self.quitreason = quitreason

    def __repr__(self):
        return f"Player(id='{self.id}', name='{self.name}')"

    def __str__(self) -> str:
        return f"Player(id='{self.id}', name='{self.name}', server_id={self.server_id}, banned={self.banned}, op={self.op}, status={self.status})"
    
    @property
    def id(self) -> int:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:int):
        if isinstance(value, str):
            self.id = int(value)
        elif isinstance(value, int):
            setattr(self, '_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def server_id(self) -> int:
        return getattr(self, '_server_id', 0)
    
    @server_id.setter
    def server_id(self, value:int):
        if value is None: self.server_id = 0
        elif isinstance(value, str):
            self.server_id = int(value)
        elif isinstance(value, int):
            setattr(self, '_server_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def level(self) -> int:
        return getattr(self, '_level', 0)
    
    @level.setter
    def level(self, value:int):
        if value is None: self.level = 0
        elif isinstance(value, str):
            self.server_id = int(value)
        elif isinstance(value, int):
            setattr(self, '_level', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def lastseen(self) -> datetime.datetime:
        return getattr(self, '_lastseen', None)
    
    @lastseen.setter
    def lastseen(self, value:int):
        if value is None: self.lastseen = 0.0
        elif isinstance(value, str):
            self.lastseen = float(value)
        elif isinstance(value, float):
            self.lastseen = datetime.datetime.fromtimestamp(value)
        elif isinstance(value, datetime.datetime):
            setattr(self, '_level', value)
        else:
            raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")

    @property
    def banned(self) -> bool:
        return getattr(self, '_banned', False)
    
    @banned.setter
    def banned(self, value:bool):
        if value is None: self.banned = False
        elif isinstance(value, str):
            self.banned = False if value == '' else True
        elif isinstance(value, bool):
            setattr(self, '_banned', value)
        else:
            raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")

    @property
    def op(self) -> bool:
        return getattr(self, '_op', False)
    
    @op.setter
    def op(self, value:bool):
        if value is None: self.op = False
        elif isinstance(value, str):
            self.op = False if value == '' else True
        elif isinstance(value, bool):
            setattr(self, '_op', value)
        else:
            raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")

    @property
    def status(self) -> Status:
        return getattr(self, '_status', Status.offline)
    
    @status.setter
    def status(self, value:bool):
        if value is None: self.status = Status.offline
        elif isinstance(value, str):
            self.status = Status[value]
        elif isinstance(value, Status):
            setattr(self, '_status', value)
        else:
            raise TypeError(f"Expected Status but got '{value.__class__.__name__}' instead")

    @property
    def ip(self) -> str|None:
        return getattr(self, '_ip', None)
    
    @ip.setter
    def ip(self, value:bool):
        if value is None: setattr(self, '_ip', None)
        else: setattr(self, '_ip', str(value))
        
    @property
    def previps(self) -> str|None:
        return getattr(self, '_previps', None)
    
    @previps.setter
    def previps(self, value:bool):
        if value is None: setattr(self, '_previps', None)
        else: setattr(self, '_previps', str(value))

    @property
    def quitreason(self) -> str|None:
        return getattr(self, '_quitreason', None)
    
    @quitreason.setter
    def quitreason(self, value:bool):
        if value is None: setattr(self, '_quitreason', None)
        else: setattr(self, '_quitreason', str(value))

    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        self.id = data.pop('id')
        self.name = data.pop('name')
        if 'server_id' in data: self.server_id = data.pop('server_id')
        if 'level' in data: self.level = data.pop('level')
        if 'lastseen' in data: self.lastseen = data.pop('lastseen')
        if 'banned' in data: self.banned = data.pop('banned')
        if 'op' in data: self.op = data.pop('op')
        if 'status' in data: self.status = data.pop('status')
        if 'ip' in data: self.ip = data.pop('ip')
        if 'previps' in data: self.previps = data.pop('previps')
        if 'quitreason' in data: self.quitreason = data.pop('quitreason')
        return self
    
    def delete(self):
        raise NotImplementedError()
    
class ServerResources:
    def __init__(self, cpu:float, memory:float, quota:int):
        setattr(self, '_cpu', cpu)
        setattr(self, '_memory', memory)
        setattr(self, '_quota', quota)

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"ServerResources(cpu={self.cpu}, memory={self.memory}, quota={self.quota})"
    
    @property
    def cpu(self) -> float:
        return getattr(self, '_cpu')

    @property
    def memory(self) -> float:
        return getattr(self, '_memory')

    @property
    def quota(self) -> int:
        return getattr(self, '_quota')
    
    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        setattr(self, '_cpu', float(data.get('cpu')))
        setattr(self, '_memory', float(data.get('memory')))
        setattr(self, '_quota', int(data.get('quota')))
        return self

class Schedule:
    def __init__(self, id:int, name:str, server_id:int=None, scheduled_ts:datetime.datetime=None, last_run_ts:datetime.datetime=None, interval:float=None, command:int=None, run_for:int=None, status:int=None, args:str=None, hidden:bool=None, **kw):
        self.id = id
        self.name = name
        self.server_id = server_id
        self.scheduled_ts = scheduled_ts
        self.last_run_ts = last_run_ts
        self.interval = interval
        self.command = command
        self.run_for = run_for
        self.status = status
        self.args = args
        self.hidden = hidden

        if 'ts' in kw: self.scheduled_ts = kw.pop('ts')
        if 'cmd' in kw: self.command = kw.pop('cmd')

    def __repr__(self):
        return f"Schedule(id='{self.id}', name='{self.name})"

    def __str__(self) -> str:
        return f"Schedule(id={self.id}, name='{self.name}', server_id={self.server_id}, scheduled_ts='{self.scheduled_ts}', last_run_ts='{self.last_run_ts}', interval={self.interval}, command={self.command}, run_for={self.run_for}, status={self.status}, args='{self.args}', hidden={self.hidden})"
    
    @property
    def id(self) -> int:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:int):
        if isinstance(value, str):
            self.id = int(value)
        elif isinstance(value, int):
            setattr(self, '_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def server_id(self) -> int:
        return getattr(self, '_server_id', 0)
    
    @server_id.setter
    def server_id(self, value:int):
        if isinstance(value, str):
            self.server_id = int(value)
        elif isinstance(value, int):
            setattr(self, '_server_id', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property    
    def scheduled_ts(self) -> datetime.datetime:
        return getattr(self, '_scheduled_ts', 0)
    
    @scheduled_ts.setter
    def scheduled_ts(self, value:datetime.datetime|int):
        if value is None: self.scheduled_ts = 0
        elif isinstance(value, int):
            self.scheduled_ts = datetime.datetime.fromtimestamp(value)
        elif isinstance(value, str):
            self.scheduled_ts = int(value)
        elif isinstance(value, datetime.datetime):
            setattr(self, '_scheduled_ts', value)
        else:
            raise TypeError(f"Expected datetime but got '{value.__class__.__name__}' instead")
    
    @property    
    def last_run_ts(self) -> datetime.datetime:
        return getattr(self, '_last_run_ts', 0)
    
    @last_run_ts.setter
    def last_run_ts(self, value:datetime.datetime|int):
        if value is None: self.scheduled_ts = 0
        elif isinstance(value, int):
            self.last_run_ts = datetime.datetime.fromtimestamp(value)
        elif isinstance(value, str):
            self.last_run_ts = int(value)
        elif isinstance(value, datetime.datetime):
            setattr(self, '_last_run_ts', value)
        else:
            raise TypeError(f"Expected datetime but got '{value.__class__.__name__}' instead")
    
    @property    
    def interval(self) -> int:
        return getattr(self, '_interval', 0)
    
    @interval.setter
    def interval(self, value:int):
        if isinstance(value, str):
            self.interval = int(value)
        elif isinstance(value, int):
            setattr(self, '_interval', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property    
    def command(self) -> int:
        return getattr(self, '_command', 0)
    
    @command.setter
    def command(self, value:int):
        if value is None: self.command = 0
        elif isinstance(value, str):
            self.command = int(value)
        elif isinstance(value, int):
            setattr(self, '_command', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property    
    def run_for(self) -> int:
        return getattr(self, '_run_for', 0)
    
    @run_for.setter
    def run_for(self, value:int):
        if value is None: self.run_for = 0
        elif isinstance(value, str):
            self.run_for = int(value)
        elif isinstance(value, int):
            setattr(self, '_run_for', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property    
    def status(self) -> int:
        return getattr(self, '_status', 0)
    
    @status.setter
    def status(self, value:ScheduleStatus):
        if value is None: self.status = ScheduleStatus.scheduled
        elif isinstance(value, str):
            self.status = int(value)
        elif isinstance(value, int):
            self.status = ScheduleStatus.from_int(value)
        elif isinstance(value, ScheduleStatus):
            setattr(self, '_status', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

    @property    
    def args(self) -> str:
        return getattr(self, '_args', '')
    
    @args.setter
    def args(self, value:str):
        setattr(self, '_args', str(value))
    
    @property    
    def hidden(self) -> bool:
        return getattr(self, '_hidden', False)
    
    @hidden.setter
    def hidden(self, value:bool):
        if value is None: self.hidden = False
        elif isinstance(value, str):
            self.hidden = True if value == '1' else False
        elif isinstance(value, bool):
            setattr(self, '_hidden', value)
        else:
            raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")

    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        self.id = data.pop('id')
        self.name = data.pop('name')
        if 'server_id' in data: self.server_id = data.pop('server_id')
        if 'scheduled_ts' in data: self.scheduled_ts = data.pop('scheduled_ts')
        if 'last_run_ts' in data: self.last_run_ts = data.pop('last_run_ts')
        if 'interval' in data: self.interval = data.pop('interval')
        if 'command' in data: self.command = data.pop('command')
        if 'run_for' in data: self.run_for = data.pop('run_for')
        if 'status' in data: self.status = data.pop('status')
        if 'args' in data: self.args = data.pop('args')
        if 'hidden' in data: self.hidden = data.pop('hidden')
        return self

    def delete(self):
        raise NotImplementedError()

class Database:
    def __init__(self, host:str, name:str, username:str, password:str, link:str):
        self.host = host
        self.name = name
        self.username = username
        self.password = password
        self.link = link

    def __repr__(self):
        return f"Database(host='{self.host}', name='{self.name}')"

    def __str__(self) -> str:
        return f"Database(host='{self.host}', name='{self.name}', username='{self.username}', link='{self.link}')"
    
    @property
    def host(self) -> str:
        return getattr(self, '_host')
    
    @host.setter
    def host(self, value:str):
        setattr(self, '_host', str(value))

    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))
        
    @property
    def username(self) -> str:
        return getattr(self, '_username')
    
    @username.setter
    def username(self, value:str):
        setattr(self, '_username', str(value))
        
    @property
    def password(self) -> str:
        return getattr(self, '_password')
    
    @password.setter
    def password(self, value:str):
        setattr(self, '_password', str(value))

    @property
    def link(self) -> str:
        return getattr(self, '_link')
    
    @link.setter
    def link(self, value:str):
        setattr(self, '_link', str(value))

    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        if 'host' in data: self.host = data.pop('host')
        if 'name' in data: self.name = data.pop('name')
        if 'username' in data: self.username = data.pop('username')
        if 'password' in data: self.password = data.pop('password')
        if 'link' in data: self.link = data.pop('link')
        return self

    def delete(self):
        raise NotImplementedError()

class Backup:
    def __init__(self, status:BackupStatus, ftp:str, message:str, file:str, time:datetime.datetime):
        self.status = status
        self.ftp = ftp
        self.message = message
        self.file = file
        self.time = time
        
    def __repr__(self):
        return f"Database(status='{self.status}', ftp='{self.ftp}', file='{self.file}')"

    def __str__(self) -> str:
        return f"Database(status='{self.status}', ftp='{self.ftp}', message='{self.message}', file='{self.file}', time='{self.time}')"
    
    @property
    def status(self) -> BackupStatus:
        return getattr(self, '_status')
    
    @status.setter
    def status(self, value:BackupStatus):
        if value is None: self.status = BackupStatus.done
        elif isinstance(value, str):
            self.status = BackupStatus[value]
        elif isinstance(value, BackupStatus):
            setattr(self, '_status', str(value))
        else:
            raise TypeError(f"Expected BackupStatus but got '{value.__class__.__name__}' instead")

    @property
    def ftp(self) -> str:
        return getattr(self, '_ftp')
    
    @ftp.setter
    def ftp(self, value:str):
        setattr(self, '_ftp', str(value))
        
    @property
    def message(self) -> str:
        return getattr(self, '_message')
    
    @message.setter
    def message(self, value:str):
        setattr(self, '_message', str(value))
        
    @property
    def file(self) -> str:
        return getattr(self, '_file')
    
    @file.setter
    def file(self, value:str):
        setattr(self, '_file', str(value))

    @property
    def time(self) -> datetime.datetime:
        return getattr(self, '_time')
    
    @time.setter
    def time(self, value:datetime.datetime|float|int):
        if isinstance(value, (float|int)):
            self.time = datetime.datetime.fromtimestamp(value)
        elif isinstance(value, str):
            self.time = float(value)
        elif isinstance(value, datetime.datetime):
            setattr(self, '_time', value)
        else:
            raise TypeError(f"Expected datetime.datetime but got '{value.__class__.__name__}' instead")

    @classmethod
    def from_json(cls, data:dict):
        self = cls.__new__(cls)
        if 'status' in data: self.status = data.pop('status')
        if 'ftp' in data: self.ftp = data.pop('ftp')
        if 'message' in data: self.message = data.pop('message')
        if 'file' in data: self.file = data.pop('file')
        if 'time' in data: self.time = data.pop('time')
        return self


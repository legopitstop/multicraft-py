import os
import datetime
import requests
import hmac
import hashlib
import json

from . import MulticraftException, User, Role, Mode, Player, Command, Server, ServerStatus, ChatMessage, ServerResources, Schedule, ScheduleStatus, Database, Backup

__all__ = ['MulticraftAPI']

class MulticraftAPI:
    def __init__(self, url:str, user:str, key:str=None):
        """
        Create a new instance of Multicraft API

        :param url: The API url. You can find common hosts in hosts.py
        :type url: str
        :param user: The username of the account to use
        :type user: str
        :param key: The API key to login with, defaults to os.getenv('KEY') if None
        :type key: str, optional
        """
        self.url = str(url)
        self.user = str(user)
        self.key = os.getenv('KEY') if key is None else str(key)
        self.user_agent = 'multicraft (https://github.com/legopitstop/multicraft-py/)'

    # Internal

    def _generateSignature(self, params:dict) -> str:
        signature = ''
        for param in self._reduce(params):
            signature += param + str(params[param])

        return hmac.new(str(self.key).encode("UTF-8"), str(signature).encode(), hashlib.sha256 ).hexdigest()
        
    def _reduce(self, obj:dict) -> dict:
        res = {}
        for k, v in obj.items():
            if isinstance(v, list): res[k] = json.dumps(v)
            else: res[k] = v
        return res

    def _call(self, method:str, params:dict={}) -> dict:
        """
        Internal method
        """
        params = self._reduce(params)
        params["_MulticraftAPIMethod"] = str(method)
        params["_MulticraftAPIUser"] = self.user
        params["_MulticraftAPIKey"] = self._generateSignature(params)

        res = requests.post(self.url, params, headers={'user-agent': self.user_agent})
        data = json.loads(res.text)
        if data.get('success'):
            return data.get('data')
        err = str(data['errors'][0]).replace('&quot;', '"')
        raise MulticraftException(err)

    # Config
    
    def set_user_agent(self, user_agent_string:str):
        """
        Set the User-Agent string to be used for all requests.

        :param user_agent_string: A string specifying the User-Agent header
        :type user_agent_string: str
        """
        self.user_agent = str(user_agent_string)

    # User functions

    def get_current_user(self) -> User:
        """
        Get the current user

        :return: The current user
        :rtype: User
        """
        res = self._call('getCurrentUser')
        return User.from_json(res['User'])

    def get_user_role(self, user_id:int, server_id:int) -> Role|None:
        """
        Get the users role

        :param user_id: The id of the user to get
        :type user_id: int
        :param server_id: The id of the server that this user belongs to
        :type server_id: int
        :return: The users role
        :rtype: Role|None
        """
        data ={
            'user_id': int(user_id),
            'server_id': int(server_id)
        }
        res = self._call('getUserRole', data)['role']
        if res == '': return None
        return Role[str(res)]

    def set_user_role(self, user_id:int, server_id:int, role:Role) -> None:
        """
        Sets the users role

        :param user_id: The id of the user to set
        :type user_id: int
        :param server_id: The id of the server that this user belongs to
        :type server_id: int
        :param role: The role to set
        :type role: Role
        """
        
        if not isinstance(role, Role) and role is not None: raise TypeError(f"Expected Role but got '{role.__class__.__name__}' instead")
        data = {
            'user_id': int(user_id),
            'server_id': int(server_id),
            'role': '' if role is None else role._value_
        }
        self._call('setUserRole', data)

    def get_user_ftp_access(self, user_id:int, server_id:int) -> Mode|None:
        """
        Get the users ftp access

        :param user_id: The id of the user to get
        :type user_id: int
        :param server_id: The id of the server that this user belongs to
        :type server_id: int
        :return: The users mode
        :rtype: Mode|None
        """
        res = self._call('getUserFtpAccess', {
            'user_id': int(user_id),
            'server_id': int(server_id)
        })['mode']
        if res == '': return None
        return Mode[str(res)]

    def set_user_ftp_access(self, user_id:int, server_id:int, mode:Mode) -> None:
        """
        Sets the users ftp access

        :param user_id: The id of the user to set
        :type user_id: int
        :param server_id: The id of the server that this user belongs to
        :type server_id: int
        :param mode: The mode to set
        :type mode: Mode
        """
        if not isinstance(mode, Mode) and mode is not None: raise TypeError(f"Expected Mode but got '{mode.__class__.__name__}' instead")
        self._call('setUserFtpAccess', {
            'user_id': int(user_id),
            'server_id': int(server_id),
            'mode': '' if mode is None else mode._value_
        })

    def get_user_id(self, name:str) -> int:
        """
        Get the users id from name

        :param name: The name of the user
        :type name: str
        :return: The id of the user
        :rtype: int
        """
        return self._call('getUserId', {
            'name': str(name)
        })['id']

    # TODO - Incorrect API key from user: USERNAME
    def get_own_api_key(self, password:str, generate=0, gauth_code:str=''):
        """
        _summary_

        :param password: _description_
        :type password: str
        :param generate: _description_, defaults to 0
        :type generate: int, optional
        :param gauth_code: _description_, defaults to ''
        :type gauth_code: str, optional
        :return: _description_
        :rtype: _type_
        """
        return self._call('getOwnApiKey', {
            'password': str(password),
            'generate': str(generate),
            'gauth_code': str(gauth_code)
        })

    # Player functions

    def list_players(self, server_id:int) -> dict[str, str]:
        """
        Get a list of all players

        :param server_id: The id of the server
        :type server_id: int
        :return: The players {ID: NAME}
        :rtype: dict
        """
        res = self._call('listPlayers', {
            'server_id': int(server_id)
        })['Players']
        return {} if isinstance(res, list) else res

    def get_player(self, player_id:int) -> Player:
        """
        Get the player from id

        :param player_id: The id of the player to get
        :type player_id: int
        :return: The player from id
        :rtype: Player
        """
        res = self._call('getPlayer', {
            'id': int(player_id)
        })['Player']
        return Player.from_json(res)

    def find_players(self, server_id:int, field:list[str], value:list[str]) -> dict[str, str]:
        """
        Get player from field-value

        Fields: name, lastseen, ip, banned, status, previps, quitreason, op

        :param server_id: The id of the server
        :type server_id: int
        :param field: The field to match
        :type field: list
        :param value: The value to match
        :type value: list
        :return: The found players {ID: NAME}
        :rtype: dict
        """
        res = self._call('findPlayers', {
            'server_id': int(server_id),
            'field': field,
            'value': value
        })['Players']
        return {} if isinstance(res, list) else res

    def update_player(self, player_id:int, field:list[str], value:list[str]) -> None:
        """
        Update this player

        :param player_id: The id of the player to update
        :type player_id: int
        :param field: The field to update
        :type field: list
        :param value: The value to update
        :type value: list
        """
        self._call('updatePlayer', {
            'id': int(player_id),
            'field': field,
            'value': value
        })

    def create_player(self, server_id:int, name:str, op_command:int=0) -> Player:
        """
        Create a new player

        :param server_id: The id of the server to create the player for
        :type server_id: int
        :param name: The name of the player to create
        :type name: str
        :param op_command: The op command, defaults to 0
        :type op_command: int, optional
        :return: The created player
        :rtype: Player
        """
        data = {
            'server_id': int(server_id),
            'name': str(name),
            'op_command': int(op_command)
        }
        id = self._call('createPlayer', data)['id']
        return Player(id, **data)

    def delete_player(self, player_id:int):
        """
        Remove a player

        :param player_id: The id of the player to remove
        :type player_id: int
        :return: _description_
        :rtype: _type_
        """
        return self._call('deletePlayer', {
            'id': int(player_id)
        })

    def assign_player_to_user(self, player_id:int, user_id:int) -> None:
        """
        Assign a player to a user

        :param player_id: The id of the player to assign
        :type player_id: int
        :param user_id: The id of the user to assign
        :type user_id: int
        """
        self._call('assignPlayerToUser', {
            'player_id': int(player_id),
            'user_id': int(user_id)
        })

    # Command functions

    def list_commands(self, server_id:int) -> dict[str,str]:
        """
        Get a list of all commands

        :param server_id: The id of the server
        :type server_id: int
        :return: The commands {ID: NAME}
        :rtype: dict
        """
        res = self._call('listCommands', {
            'server_id': int(server_id)
        })['Commands']
        return {} if isinstance(res, list) else res

    def find_commands(self, server_id:int, field:list[str], value:list[str]) -> dict[int, str]:
        """
        Get command from field-value

        Fields: name, chat, response, run, prereq

        :param server_id: The id of the server
        :type server_id: int
        :param field: The field to match
        :type field: list
        :param value: The value to match
        :type value: list
        :return: The found commands {ID: NAME}
        :rtype: dict
        """
        res = self._call('findCommands', {
            'server_id': int(server_id),
            'field': field,
            'value': value
        })['Commands']
        return {} if isinstance(res, list) else res

    def get_command(self, command_id:int) -> Command:
        """
        Get the command from id

        :param command_id: The id of the command to get
        :type command_id: int
        :return: The command from id
        :rtype: Command
        """
        res = self._call('getCommand', {
            'id': int(command_id)
        })['Command']
        return Command.from_json(res)

    def update_command(self, command_id:int, field:list[str], value:list[str]) -> None:
        """
        Update this command

        :param command_id: The id of the command to update
        :type command_id: int
        :param field: The field to update
        :type field: list
        :param value: The value to update
        :type value: list
        """
        self._call('updateCommand', {
            'id': int(command_id),
            'field': field,
            'value': value
        })

    def create_command(self, server_id:int, name:str, role:Role, chat:str, response:str, run:str) -> Command:
        """
        Create a new command

        :param server_id: The id of the server to create the command for
        :type server_id: int
        :param name: The name of the command
        :type name: str
        :param role: The role of the command
        :type role: Role
        :param chat: The chat command to run
        :type chat: str
        :param response: The response text
        :type response: str
        :param run: The command to run
        :type run: str
        :return: The created command
        :rtype: Command
        """
        if not isinstance(role, Role): raise TypeError(f"Expected Role but got '{role.__class__.__name__}' instead")
        data = {
            'server_id': int(server_id),
            'name': str(name),
            'role': role._value_,
            'chat': str(chat),
            'response': str(response),
            'run': str(run)
        }
        id = self._call('createCommand', data)['id']
        return Command(id, **data)

    def delete_command(self, command_id:int) -> None:
        """
        Remove a command

        :param command_id: The id of the command to remove
        :type command_id: int
        """
        self._call('deleteCommand', {
            'id': int(command_id)
        })

    # Server functions

    def list_servers_by_owner(self, user_id:int) -> dict[str,str]:
        """
        Get a list of all servers that this user owns

        :param user_id: The id of the user
        :type user_id: int
        :return: The servers that this user owns {ID: NAME}
        :rtype: dict
        """
        res = self._call('listServersByOwner', {
            'user_id': int(user_id)
        })['Servers']
        return {} if isinstance(res, list) else res

    # TODO - Access denied
    def list_servers_by_connection(self, connection_id:int):
        res = self._call('listServersByConnection', {
            'connection_id': int(connection_id)
        })
        return res

    # TODO Access denied
    def update_server(self, server_id:int, field:list[str], value:list[str]):
        """
        Update this server

        :param server_id: The id of the server to update
        :type server_id: int
        :param field: The field to update
        :type field: list
        :param value: The value to update
        :type value: list
        :return: The updated server
        :rtype: Server
        """
        return self._call('updateServer', {
            'id': int(server_id),
            'field': field,
            'value': value
        })

    def start_server(self, server_id:int) -> None:
        """
        Start this server

        :param server_id: The id of the server to start
        :type server_id: int
        """
        self._call('startServer', {
            'id': int(server_id)
        })

    def stop_server(self, server_id:int) -> None:
        """
        Stop this server

        :param server_id: The id of the server to stop
        :type server_id: int
        """
        self._call('stopServer', {
            'id': int(server_id)
        })

    def restart_server(self, server_id:int) -> None:
        """
        Restart this server

        :param server_id: The id of the server to restart
        :type server_id: int
        """
        self._call('restartServer', {
            'id': int(server_id)
        })

    def kill_server(self, server_id:int) -> None:
        """
        Kill this server

        :param server_id: The id of the server to kill
        :type server_id: int
        """
        self._call('killServer', {
            'id': int(server_id)
        })

    def send_console_command(self, server_id:int, command:str) -> None:
        """
        Send this command to console

        :param server_id: The id of the server to send the command to
        :type server_id: int
        :param command: The command to run
        :type command: str
        """
        self._call('sendConsoleCommand', {
            'server_id': int(server_id),
            'command': str(command)
        })

    def run_command(self, server_id:int, command_id:int, run_for:int=0) -> None:
        """
        Run a command from id

        :param server_id: The id of the server that this command belongs to
        :type server_id: int
        :param command_id: The id of the command to run
        :type command_id: int
        :param run_for: The id of the player to run this command for, defaults to 0
        :type run_for: int, optional
        """
        self._call('runCommand', {
            'server_id': int(server_id),
            'command_id': int(command_id),
            'run_for': int(run_for)
        })

    def clear_server_log(self, server_id:int) -> None:
        """
        Clear the server log history

        :param server_id: The id of the server log to clear
        :type server_id: int
        """
        self._call('clearServerLog', {
            'id': int(server_id)
        })

    def clear_server_chat(self, server_id:int) -> None:
        """
        Clear the server chat history

        :param server_id: The id of the server chat to clear
        :type server_id: int
        """
        self._call('clearServerChat', {
            'id': int(server_id)
        })

    def get_server(self, server_id:int) -> Server:
        """
        Get the server from id

        :param server_id: The id of the server to get
        :type server_id: int
        :return: The server from id
        :rtype: Server
        """
        res = self._call('getServer', {
            'id': int(server_id)
        })
        res['Server']['id'] = server_id
        return Server.from_json(res['Server'])

    def get_server_status(self, server_id:int, player_list:bool=False) -> ServerStatus:
        """
        Get the server's status

        :param server_id: The id of the server
        :type server_id: int
        :param player_list: Whether or not it should include a list of online players, defaults to False
        :type player_list: bool, optional
        :return: The ServerStatus
        :rtype: ServerStatus
        """
        if not isinstance(player_list, bool): raise TypeError(f"Expected bool but got '{player_list.__class__.__name__}' instead")
        res = self._call('getServerStatus', {
            'id': int(server_id),
            'player_list': 1 if player_list else 0
        })
        return ServerStatus.from_json(res)

    def get_server_log(self, server_id:int) -> list[str]:
        """
        Get the server's log

        :param server_id: The id of the server
        :type server_id: int
        :return: The server's log
        :rtype: list[str]
        """
        res = self._call('getServerLog', {
            'id': int(server_id)
        })
        return [str(x['line']) for x in res]

    def get_server_chat(self, server_id:int) -> list[ChatMessage]:
        """
        Get the server's chat

        :param server_id: The id of the server
        :type server_id: int
        :return: The server's chat
        :rtype: list[ChatMessage]
        """
        res = self._call('getServerChat', {
            'id': int(server_id)
        })
        return [ChatMessage.from_json(x) for x in res]

    def get_server_resources(self, server_id:int) -> ServerResources:
        """
        Get the server's resources

        :param server_id: The id of the server
        :type server_id: int
        :return: The server's resources
        :rtype: ServerResources
        """
        res = self._call('getServerResources', {
            'id': int(server_id)
        })
        return ServerResources.from_json(res)

    # Schedule functions

    def list_schedules(self, server_id:int) -> dict[str, str]:
        """
        Get a list of all schedules

        :param server_id: The id of the server
        :type server_id: int
        :return: The schedules {ID: NAME}
        :rtype: dict
        """
        res = self._call('listSchedules', {
            'server_id': int(server_id)
        })['Schedules']
        return {} if isinstance(res, list) else res

    def find_schedules(self, server_id:int, field:list[str], value:list[str]) -> dict[str,str]:
        """
        Get schedule from field-value

        Fields: name, interval, status, command, args

        :param server_id: The id of the server
        :type server_id: int
        :param field: The field to match
        :type field: list
        :param value: The value to match
        :type value: list
        :return: The found schedules {ID: NAME}
        :rtype: dict
        """
        res = self._call('findSchedules', {
            'server_id': int(server_id),
            'field': field,
            'value': value
        })['Schedules']
        return {} if isinstance(res, list) else res

    def update_schedule(self, schedule_id:int, field:list[str], value:list[str]) -> None:
        """
        Update this schedule

        :param schedule_id: The id of the schedule to update
        :type schedule_id: int
        :param field: The field to update
        :type field: list
        :param value: The value to update
        :type value: list
        """
        self._call('updateSchedule', {
            'id': int(schedule_id),
            'field': field,
            'value': value
        })

    def get_schedule(self, schedule_id:int) -> Schedule:
        """
        Get the schedule from id

        :param schedule_id: The id of the schedule to get
        :type schedule_id: int
        :return: The schedule from id
        :rtype: Schedule
        """
        res = self._call('getSchedule', {
            'id': int(schedule_id)
        })['Schedule']
        return Schedule.from_json(res)

    def create_schedule(self, server_id:int, name:str, ts:datetime.datetime,  command:int, interval:int=0, status:ScheduleStatus=ScheduleStatus.scheduled, _for:int=0) -> Schedule:
        """
        Create a new schedule

        :param server_id: The id of the server to create the schedule for
        :type server_id: int
        :param name: The name of the schedule
        :type name: str
        :param ts: The datetime to run this schedule
        :type ts: datetime.datetime
        :param command: The id of the command to run for this schedule
        :type command: int
        :param interval: Time (in seconds) before it runs this schedule again, defaults to 0
        :type interval: int, optional
        :param status: The schedule's status, defaults to ScheduleStatus.scheduled
        :type status: ScheduleStatus, optional
        :param _for: The player to run this schedule for, defaults to 0
        :type _for: int, optional
        :return: The created schedule
        :rtype: Schedule
        """
        if not isinstance(ts, datetime.datetime): raise TypeError(f"Expected datetime.datetime but got '{ts.__class__.__name__}' instead")
        if not isinstance(status, ScheduleStatus): raise TypeError(f"Expected ScheduleStatus but got '{ts.__class__.__name__}' instead")
        data = {
            'server_id': int(server_id),
            'name': str(name),
            'ts': int(ts.timestamp()),
            'interval': int(interval),
            'cmd':int(command),
            'status': status._value_,
            'for': int(_for)
        }
        id = self._call('createSchedule', data)['id']
        return Schedule(id, **data)

    def delete_schedule(self, schedule_id:int) -> None:
        """
        Remove a schedule

        :param schedule_id: The id of the schedule to remove
        :type schedule_id: int
        """
        return self._call('deleteSchedule', {
            'id': int(schedule_id)
        })

    # Database functions

    def get_database_info(self, server_id:int) -> Database:
        """
        Get info about the database

        :param server_id: The id of the server to get the database from
        :type server_id: int
        :return: Info about the database
        :rtype: Database
        """
        res = self._call('getDatabaseInfo', {
            'server_id': int(server_id)
        })
        return Database.from_json(res)

    def create_database(self, server_id:int, name:str=None, password:str=None) -> Database:
        """
        Create a new database (Limit of one database per server)

        :param server_id: The id of the server to create the database for
        :type server_id: int
        :param name: The name of the database (Autogenerated for some hosts), defaults to None
        :type name: str, optional
        :param password: The password of the database (Autogenerated for some hosts), defaults to None
        :type password: str, optional
        :return: The created database
        :rtype: Database
        """
        data = {
            'server_id': int(server_id),
            'name': str(name),
            'password': str(password)
        }
        res = self._call('createDatabase', data)
        return Database.from_json(res)

    def change_database_password(self, server_id:int, database_id:int=None, password:str=None) -> Database:
        """
        Change the database password

        :param server_id: The id of the server that the database belongs to
        :type server_id: int
        :param database_id: The id of the database (For some hosts this is the same as the server id), defaults to server_id if None
        :type database_id: int
        :param password: The new password for the database (Autogenerated for some hosts), defaults to None
        :type password: str, optional
        :return: The updated database with the new password
        :rtype: Database
        """
        res = self._call('changeDatabasePassword', {
            'server_id': int(server_id),
            'database_id': int(server_id) if database_id is None else int(database_id),
            'password': str(password)
        })
        return Database.from_json(res)

    def delete_database(self, server_id:int, database_id:int=None) -> None:
        """
        Remove a database

        :param server_id: The id of the server that this database belongs to
        :type server_id: int
        :param database_id: The id of the database (For some hosts this is the same as the server id), defaults to server_id if None
        :type database_id: int
        """
        self._call('deleteDatabase', {
            'server_id': int(server_id),
            'database_id': int(server_id) if database_id is None else int(database_id)
        })

    def start_server_backup(self, server_id:int) -> None:
        """
        Starts a backup of the server

        :param server_id: The id of the server to backup
        :type server_id: int
        """
        self._call('startServerBackup', {
            'id': int(server_id)
        })

    def get_server_backup_status(self, server_id:int) -> Backup:
        """
        Get the backup status of the server

        :param server_id: The id of the server
        :type server_id: int
        :return: The backup status of the server
        :rtype: Backup
        """
        res = self._call('getServerBackupStatus', {
            'id': int(server_id)
        })
        return Backup.from_json(res)

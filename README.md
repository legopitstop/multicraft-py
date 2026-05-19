# multicraft

![Tests](https://github.com/legopitstop/multicraft-py/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/multicraft)](https://pypi.org/project/multicraft/)
[![Python](https://img.shields.io/pypi/pyversions/multicraft)](https://www.python.org/downloads/)
![Downloads](https://img.shields.io/pypi/dm/multicraft)
![Status](https://img.shields.io/pypi/status/multicraft)
[![Issues](https://img.shields.io/github/issues/legopitstop/multicraft-py)](https://github.com/legopitstop/multicraft-py/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Interact with your Minecraft server from hosts that use [Multicraft](https://www.multicraft.org/) in Python.

## Installation

Install the module with pip:

```bat
pip3 install multicraft
```

Update existing installation: `pip3 install multicraft --upgrade`

## Links

- [Documentation](https://docs.lpsmods.dev/multicraft)
- [Source Code](https://github.com/legopitstop/multicraft-py)

## Features

- Includes a handful of common multicraft hosts.
- Manage users, players, commands, schedules, and databases.
- Start, stop, or restart your server.
- Run console commands (give, kill, whitelist, op, etc)
- Read your server's current CPU and memory usage.
- Send a chat message.

See the [docs](https://github.com/legopitstop/multicraft-py/wiki) for more information.

## Dependencies

| Name                                           | Description                                      |
| ---------------------------------------------- | ------------------------------------------------ |
| [requests](https://pypi.org/project/requests/) | Requests is a simple, yet elegant, HTTP library. |
| [pydantic](https://pypi.org/project/pydantic/) | Data validation using Python type hints          |

## Example

```py
from multicraft import MulticraftAPI
from multicraft.hosts import BISECT_PREMIUM

api = MulticraftAPI(
    host = BISECT_PREMIUM,
    user = 'username',
    key = 'apiKey'
)

owner = api.get_user_id(api.user)

owned_servers = api.list_servers_by_owner(owner)
print(owned_servers)

for id in owned_servers.keys():
    server = api.get_server(id)
    print(server)
```

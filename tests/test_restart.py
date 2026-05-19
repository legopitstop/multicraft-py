"""
Restart all servers only if no players are online or the server is offline
"""

from multicraft import MulticraftAPI, Status
from multicraft.hosts import BISECT_PREMIUM


def test_restart():
    api = MulticraftAPI(host=BISECT_PREMIUM)

    owner = api.get_user_id(api.host._user)

    owned_servers = api.list_servers_by_owner(owner)
    for id in owned_servers.keys():
        server = api.get_server(id)
        print(server)

        status = api.get_server_status(server.id)
        if status.online_players == 0 and status.status == Status.online:
            print("RESTARTING!")
            api.restart_server(server.id)

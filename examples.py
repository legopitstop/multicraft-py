import multicraft

api = multicraft.MulticraftAPI(
    url = 'https://localhost/api.php',
    user = 'username',
    key = 'apiKey'
)

def examples():
    owned_servers = api.list_servers_by_owner(api.get_user_id(api.user))
    print(owned_servers)

    connection_servers = api.list_servers_by_connection(1)
    print(connection_servers)

examples()
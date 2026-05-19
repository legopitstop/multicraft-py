import multicraft
from multicraft.contrib.hosts import BISECT
import dotenv

dotenv.load_dotenv()


def test():
    api = multicraft.MulticraftAPI(BISECT, "legopitstop")

    # Get server
    server = api.get_server(141815)
    print(server)

    # send console command
    res = api.send_console_command(server.id, "say Hello from multicraft.py!")
    print(res)

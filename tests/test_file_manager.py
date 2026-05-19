from multicraft import MulticraftAPI
from multicraft.contrib.hosts import BISECT
from pysftp import CnOpts
import dotenv

dotenv.load_dotenv()


def test_file_manager():
    api = MulticraftAPI(host=BISECT)

    # Not recomended for prod
    cnopts = CnOpts()
    cnopts.hostkeys = None

    with api.get_file_manager(cnopts=cnopts) as fd:
        print("Connection succesfully stablished ... ")

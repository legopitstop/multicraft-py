"""
All known hosts that use multicraft
"""

__all__ = ["BISECT"]

from multicraft.core.model import Host

BISECT = Host(
    homepage="https://games.bisecthosting.com",
    api_url="https://games.bisecthosting.com/api.php",
    sftp_host="gamesdal56.bisecthosting.com",
    sftp_port=2022,
)

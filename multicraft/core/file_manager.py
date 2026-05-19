__all__ = ["FileManager"]

from typing import Optional
import os

try:
    from pysftp import Connection
except ImportError:
    raise ImportError(
        "Missing optional dependency 'pysftp'.  Use pip or conda to install pysftp."
    )

from .. import Host


class FileManager(Connection):
    def __init__(self, host: Host, username: str, password: Optional[str] = None, **kw):
        self.host = host
        _username = username
        _password = str(password) if password else os.getenv("SFTP_PASSWORD")

        Connection.__init__(
            self,
            host=host.sftp_host,
            username=_username,
            password=_password,
            port=self.host.sftp_port,
            **kw,
        )

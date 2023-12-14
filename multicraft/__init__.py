"""
Interact with your Minecraft server from hosts that use [Multicraft](https://www.multicraft.org/) using Python.
"""
class MulticraftException(Exception): pass

__version__ = '0.0.2'

from .hosts import *
from .model import *
from .api import MulticraftAPI
from .app import MulticraftApp

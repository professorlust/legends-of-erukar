from .model import *
from .Connector import Connector

__all__ = ["Player", "Connector", "Character", "Item", "Modifier", "EquippedItem"]

import logging
SchemaLogger = logging.getLogger('schema')
SchemaLogger.setLevel(logging.INFO)
fh = logging.FileHandler('schema.log')
SchemaLogger.addHandler(fh)

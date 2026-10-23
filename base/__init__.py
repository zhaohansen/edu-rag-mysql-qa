import os
import sys

inner_name = os.path.dirname(__file__)
project_root = os.path.dirname(inner_name)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from .config import Config
from .logger import logger


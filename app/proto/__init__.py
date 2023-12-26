# =================xGLOBAL_IMPORTS
import sys
import os
import json
import unittest
import datetime
import re
import logging
import typing
import typing_extensions

__all__ = ['app.py', 'process.py']

import os
import sys
import json
import unittest
import datetime
import re

# ===================GLOBAL_FUNCTIONS
from app import main
print(f"cognos init in {os.getcwd()}")
sys.path.append(os.getcwd())
main()

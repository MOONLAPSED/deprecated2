import logging
from pathlib import Path
import sys
import os


if 'runtime' not in logging.Logger.manager.loggerDict:
    logging.basicConfig(level=logging.INFO)
runtime = logging.getLogger('runtime')

def main() -> None:
    runtime.info(f"'runtime|{__file__}| invoked from {Path(__file__).resolve().parent}||")
    # evaluate the runtime state, invoked from ..main.py? via src.launch? Via a symlink or custom launcher?
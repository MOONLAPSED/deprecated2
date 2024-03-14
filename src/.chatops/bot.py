""" ChatOps Bot provisioning: flottbot on go """

from types import SimpleNamespace
from . import flashbot


flashbot = SimpleNamespace()
flashbot.__name__ = 'flashbot'
flashbot.__file__ = '/workspaces/cognos/src/flash/bot.py'


entry_points = {
    "bot.plugins": [
        "flash{src} = flashbot.bot:FlashBot",
        "commit{flash} = flashbot.bot:FlashCommit",
    ]
}
from errbot import BotPlugin, botcmd
from flash import FlashBot, FlashCommit
from main import main
"""only packages have the __path__ attribute on the module object, so the module must be a package"""
class FlashBot(BotPlugin):
    def activate(self):
        super().activate()
        self.flashbot = FlashBot()
        self.flashcommit = FlashCommit()

    @botcmd
    def flash(self, msg, args):
        """Flash the codebase"""
        return self.flashbot.flash()
    @botcmd
    def commit(self, msg, args):
        """Commit the flashes to the knowledge base"""
        return self.flashcommit.commit()
    @botcmd
    def bfs(self, msg, args):
        """Breadth-first search of the knowledge base"""
        return self.flashbot.bfs(args)
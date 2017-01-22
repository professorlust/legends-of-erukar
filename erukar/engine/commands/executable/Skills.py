from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms import Lifeform

class Skills(Command):
    aliases = ['skills', 'my skills']

    def execute(self, *_):
        self.append_result(self.sender_uid, 'Skills')
        return self.succeed()


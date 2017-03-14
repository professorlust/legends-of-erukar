from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms import Lifeform

class Skills(Command):
    aliases = ['skills', 'my skills']

    def execute(self, *_):
        descriptions = '\n'.join([c.on_skills() for c in self.find_player().lifeform().skills])

        self.append_result(self.sender_uid, '\n'.join(['Skills', '-'*12 + '\n', descriptions]))
        return self.succeed()


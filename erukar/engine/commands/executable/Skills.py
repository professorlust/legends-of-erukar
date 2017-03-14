from erukar.engine.commands.Command import Command
from erukar.engine.lifeforms import Lifeform

class Skills(Command):
    aliases = ['skills', 'my skills']

    def execute(self, *_):
        target = self.find_player().lifeform()
        descriptions = '\n\n'.join([c.on_skills() for c in target.skills])

        self.append_result(self.sender_uid, '\n'.join(['Skills', '='*16, descriptions]))
        return self.succeed()

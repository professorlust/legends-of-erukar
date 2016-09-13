from erukar.engine.commands.Command import Command
import erukar

class Levelup(Command):
    aliases = ['level', 'levelup']

    def execute(self, *_):
        print('Level up!')

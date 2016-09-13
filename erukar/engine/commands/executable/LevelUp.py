from erukar.engine.commands.Command import Command
import erukar

class LevelUp(Command):
    aliases = ['level']

    def execute(self, *_):
        print('Level up!')

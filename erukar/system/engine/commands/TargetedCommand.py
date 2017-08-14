from .Command import Command
from .CommandResult import CommandResult

class TargetedCommand(Command):
    def process_args(self):
        if not self.args: 
            raise Exception('Cannot process args -- Command\'s args are undefined')

        if 'target' in self.args:
            self.find_target()

        super().process_args()

    def find_target(self):
        for interaction in getattr(self, 'interactions', []):
            if str(interaction.uuid) == self.args['target']:
                self.args['target'] = interaction

    def execute(self):
        self.process_args()
        return self.perform()

    def succeed_with_new_interaction(self, interaction):
        result = CommandResult(True, self, self.results, self.dirtied_characters)
        result.interaction = interaction
        self.sever()
        return result

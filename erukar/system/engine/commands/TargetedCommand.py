from .Command import Command
from .CommandResult import CommandResult

class TargetedCommand(Command):
    def process_args(self):
        if not self.args: 
            raise Exception('Cannot process args -- Command\'s args are undefined')

        if 'interaction' in self.args:
            self.find_interaction()

        for argument in self.args:
            if 'interaction' not in self.args or not self.args['interaction']: break

            try: arg_uuid = self.get_uuid_for_argument(argument)
            except: continue

            obj = self.args['interaction'].main_npc.get_object_by_uuid(arg_uuid)
            if obj and self.object_index_is_valid(obj):
                self.args[argument] = obj

        super().process_args()

    def find_interaction(self):
        for interaction in getattr(self, 'interactions', []):
            if str(interaction.uuid) == self.args['interaction']:
                self.args['interaction'] = interaction

    def execute(self):
        self.process_args()
        return self.perform()

    def succeed_with_new_interaction(self, interaction):
        result = CommandResult(True, self, self.results, self.dirtied_characters)
        result.interaction = interaction
        self.sever()
        return result

    def check_for_failure_on_interaction(self):
        if self.invalid('interaction'): 
            return self.fail('Interaction not specified.')
        
        if not isinstance(self.args['interaction'], Interaction):
            return self.fail('Target is not an interaction')

        if self.args['interaction'].ended:
            return self.fail('Target Interaction has already ended')

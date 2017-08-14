from ..ActionCommand import ActionCommand
from ..targetable.Start import Start
from erukar.system.engine import Npc

class Interact(ActionCommand):
    ActionPointCost = 0

    '''
    requires:
        target
    '''

    def perform(self):
        if self.invalid('target'): return self.fail('No target was found')

        if isinstance(self.args['target'], Npc):
            return self.exec_start_interaction()

        return self.fail('No target was valid.')

    def exec_start_interaction(self):
        st = self.copy_to_cmd(Start())
        return st.execute()

    def copy_to_cmd(self, new_cmd):
        new_cmd.args = self.args.copy()
        new_cmd.player_info = self.player_info
        new_cmd.world = self.world
        return new_cmd

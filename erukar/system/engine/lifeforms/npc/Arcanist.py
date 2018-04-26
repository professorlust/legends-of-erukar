from .NpcTemplate import NpcTemplate

class Arcanist(NpcTemplate):
    def interaction_text(self):
        return 'Purchase Arcane Enhancements from {}'.format(self.npc.alias())

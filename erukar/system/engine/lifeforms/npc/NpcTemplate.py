class NpcTemplate:
    is_interactive = True

    def __init__(self, world):
        self.world = world
        self.npc = None

    def get_state(self, for_player):
        return ('default', 'If you see this, you have seen a bug')

    def apply(self, npc):
        npc.templates.append(self)
        self.npc = npc

    def interaction_text(self):
        return 'Interact with {}'.format(self.npc.alias())

    def standard_inventory(self):
        return []

    def player_stop(self, player):
        pass

class NpcTemplate:
    is_interactive = True

    def get_state(self, npc, for_player):
        return ('default', 'If you see this, you have seen a bug')

    def apply(self, npc):
        npc.templates.append(self)

    def interaction_text(self, npc):
        return 'Interact with {}'.format(npc.alias())

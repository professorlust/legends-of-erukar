class NpcTemplate:
    def get_state(self, npc):
        return ('default', 'If you see this, you have seen a bug')

    def apply(self, npc):
        npc.templates.append(self)
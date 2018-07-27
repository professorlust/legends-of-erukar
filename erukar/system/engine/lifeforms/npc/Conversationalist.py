from .NpcTemplate import NpcTemplate


class Conversationalist(NpcTemplate):
    def __init__(self, world):
        super().__init__(world)

    def interaction_text(self):
        return 'Talk with {}'.format(self.npc.alias())

    def get_state(self, for_player):
        return {
            'type': 'Conversation',
            'title': 'Conversation with {}'.format(self.npc.alias()),
            'response': self.npc.conversation.response(for_player),
            'choices': self.get_choices(for_player)
        }

    def get_choices(self, for_player):
        choices = []
        for option in self.npc.conversation.get_choices(for_player):
            choices.append({
                'id': option[0],
                'choice': option[1]
            })
        if len(choices) == 0:
            return [{
                'id': 'exit',
                'choice': 'EXIT'
            }]
        return choices

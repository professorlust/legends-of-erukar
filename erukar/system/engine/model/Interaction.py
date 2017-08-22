from .ErukarObject import ErukarObject
from .PlayerNode import PlayerNode
import uuid

class Interaction(ErukarObject):
    '''Base class for all interactions: conversations, shops, etc'''
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.involved = []
        self.leaving = []
        self.main_npc = None
        self.ended = False
        self.results = {}

    def mark_for_exit(self, participant):
        try: self.involved.remove(participant)
        except ValueError: return
        self.leaving.append(participant)

    def player_participants(self):
        for party in self.involved:
            if isinstance(party, PlayerNode):
                yield party

    def clean(self):
        self.leaving = []
        self.ended = not (self.ended or any(self.involved))

    def get_result_for(self, node):
        results = self.main_npc.get_state()
        results['log'] = self.results.pop(node, [])
        return results

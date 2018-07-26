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
        try:
            self.involved.remove(participant)
        except ValueError:
            self.results[participant] = ['You are not in this interaction']
            return
        self.leaving.append(participant)
        self.results[participant] = ['You have left this interaction']

    def player_participants(self):
        for party in self.involved:
            if isinstance(party, PlayerNode):
                yield party

    def clean(self):
        self.leaving = []
        self.ended = not (self.ended or any(self.involved))

    def get_result_for(self, node):
        results = self.main_npc.get_state(node.lifeform())
        results['log'] = self.results.pop(node, [])
        return results

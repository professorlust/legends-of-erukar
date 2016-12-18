from erukar.engine.model.Condition import Condition
from erukar.engine.environment.Aura import Aura

class Dreadful(Condition):
    Incapacitates = False
    BriefDescription = "You feel a sense of great dread."
    SelfAuraDescription = ""

    def __init__(self, target):
        super().__init__(target)

    def initiate_aura(self):
        self.aura = Aura(self.target.current_room)
        self.aura.BriefDescription = self.BriefDescription
        self.aura.initiator = self.target
        self.target.initiate_aura(self.aura)

    def do_end_of_turn_effect(self):
        if not hasattr(self, 'aura'):
            self.initiate_aura()
        self.aura.location = self.target.current_room
        return ''

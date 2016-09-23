from erukar.engine.model.Affliction import Affliction
from erukar.engine.environment.Aura import Aura

class Dreadful(Affliction):
    Incapacitates = False
    BriefDescription = "You feel a sense of great dread."
    SelfAuraDescription = ""

    def __init__(self, afflicted):
        super().__init__(afflicted)

    def initiate_aura(self):
        self.aura = Aura(self.afflicted.current_room)
        self.aura.BriefDescription = self.BriefDescription
        self.aura.initiator = self.afflicted
        self.afflicted.initiate_aura(self.aura)

    def do_end_of_turn_effect(self):
        if not hasattr(self, 'aura'):
            self.initiate_aura()
        self.aura.location = self.afflicted.current_room
        return ''

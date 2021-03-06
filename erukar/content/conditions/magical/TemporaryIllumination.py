from erukar.system.engine import Condition, Aura

class TemporaryIllumination(Condition):
    Incapacitates = False
    BriefDescription = "A clean, white light brightly shines from the {relative_direction}."
    SelfAuraDescription = "Light radiates from your {, greatly illuminating the room."

    def __init__(self, target):
        super().__init__(target)
        self.light_power = 4

    def initiate_aura(self):
        self.aura = Aura(self.target.current_room)
        self.aura.BriefDescription = self.BriefDescription
        self.aura.initiator = self.target
        self.aura.modify_light = True
        self.aura.blocked_by_walls = True
        self.target.initiate_aura(self.aura)

    def tick(self, cmd):
        self.timer -= 1
        if self.timer <= 0:
            self.aura.is_expired = True
            self.target.conditions.remove(self)
            cmd.append_result(
                self.target,
                'Your light disappears!')

    def do_end_of_turn_effect(self, cmd):
        if not hasattr(self, 'aura'):
            self.initiate_aura()
        self.aura.location = self.target.current_room

    def modify_light(self, decay=1):
        return self.light_power * decay

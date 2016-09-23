from erukar.game.modifiers.ItemModifier import ItemModifier
from erukar.engine.environment.Aura import Aura

class LightManipulatingItemModifier(ItemModifier):
    AuraDescription = "You see light emanating from the {relative_direction}."

    def apply_to(self, item):
        super().apply_to(item)
        self.aura = None
        self.aura_strength = 2
        self.aura_decay = 0.5
        self.light_power = 0.2

    def on_start(self, room):
        self.start_aura(room)

    def on_take(self, lifeform):
        self.stop_aura()

    def on_drop(self, room, lifeform):
        self.start_aura(room)

    def on_move(self, room):
        if self.aura:
            self.aura.location = room

    def on_equip(self, lifeform):
        self.start_aura(lifeform)

    def start_aura(self, initiator):
        self.aura = Aura((0,0), self.aura_strength, self.aura_decay)
        self.aura.blocked_by_walls = True
        self.aura.modify_light = self.modify_light
        self.aura.BriefDescription = self.AuraDescription
        initiator.initiate_aura(self.aura)

    def on_unequip(self, lifeform):
        self.stop_aura()

    def stop_aura(self):
        if self.aura:
            self.aura.is_expired = True
            self.aura = None

    def modify_light(self):
        return self.light_power

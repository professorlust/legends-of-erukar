from erukar.game.modifiers.ItemModifier import ItemModifier
from erukar.engine.environment.Aura import Aura

class LightManipulatingItemModifier(ItemModifier):
    def apply_to(self, item):
        super().apply_to(item)
        self.aura = None
        self.aura_strength = 2
        self.aura_decay = 0.5
        self.light_power = 0.2

    def on_move(self, room):
        if self.aura:
            self.aura.location = room.coordinates

    def on_equip(self, lifeform):
        self.aura = Aura((0,0), self.aura_strength, self.aura_decay)
        self.aura.modify_light = self.modify_light
        lifeform.initiate_aura(self.aura)

    def on_unequip(self, lifeform):
        if self.aura:
            self.aura.is_expired = True
            self.aura = None

    def modify_light(self):
        return self.light_power

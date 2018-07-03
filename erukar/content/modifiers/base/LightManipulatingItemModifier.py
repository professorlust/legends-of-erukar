from .AuraModifier import AuraModifier
from erukar.system.engine import Aura, Observation, Dungeon, Lifeform


class LightManipulatingItemModifier(AuraModifier):
    def modify_aura(self):
        self.aura.modify_light = self.modify_light

    def modify_light(self, loc):
        if not self.aura:
            return 0
        return self.aura.strength_at(loc)

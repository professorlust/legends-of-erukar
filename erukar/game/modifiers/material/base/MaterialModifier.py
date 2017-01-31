from erukar.engine.model import Modifier
from erukar.game.modifiers.ItemModifier import ItemModifier
from erukar.engine.inventory import Armor
from erukar.engine.inventory import Weapon

class MaterialModifier(ItemModifier):
    PermissionType = Modifier.ALL_PERMITTED_BUT_NOT_PROHIBITED
    PermittedEntities = [Weapon, Armor]
    
    FlexibilityMultiplier = 1.0
    WeightMultiplier = 1.0
    DurabilityMultiplier = 1.0
    MitigationMultipliers = {
        # type, mitigation percent, glancing range
    }

    def apply_to(self, entity):
        entity.material = self
        # Adjust Weight and Durability
        # Adjust weight
        # Adjust Movement Penalty

        if issubclass(type(entity), Weapon):
            return
        if issubclass(type(entity), Armor):
            self.apply_to_armor(entity)

    def mitigation_multiplier_for(self, dtype):
        if dtype in self.MitigationMultipliers:
            return self.MitigationMultipliers[dtype]
        return (1,1)

    def apply_to_armor(self, entity):
        # Adjust Mitigations and Deflecti
        pass
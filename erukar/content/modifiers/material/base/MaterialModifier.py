from ...base.ItemModifier import ItemModifier
from erukar.system.engine import Modifier, Weapon, Armor


class MaterialModifier(ItemModifier):
    PermissionType = Modifier.ALL_PERMITTED_BUT_NOT_PROHIBITED
    PermittedEntities = []

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

    def on_alias(self, current_alias):
        return ' '.join([self.InventoryName, current_alias])

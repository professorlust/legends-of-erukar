from erukar.system.engine import Modifier, Weapon
from .ItemModifier import ItemModifier

class WeaponMod(ItemModifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = []

    def apply_to(self, weapon):
        super().apply_to(weapon)

    def on_alias(self, alias):
        return '{} {}'.format(self.InventoryName, alias)

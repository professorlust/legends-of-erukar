from erukar.engine.model import Modifier
from .ItemModifier import ItemModifier
from erukar.engine.inventory import Weapon

class WeaponMod(ItemModifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Weapon]

    def apply_to(self, weapon):
        super().apply_to(weapon)

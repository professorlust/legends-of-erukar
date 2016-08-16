from .ItemModifier import ItemModifier
from erukar.engine.inventory import Weapon

class WeaponMod(ItemModifier):
    def __init__(self):
        super().__init__()
        self.permission_type = Modifier.ALL_PERMITTED
        self.permitted_entities = [Weapon]

    def apply_to(self, weapon):
        super().apply_to(weapon)

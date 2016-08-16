from .ItemModifier import ItemModifier
from erukar.engine.inventory import Armor
from erukar.engine.inventory import Weapon

class MaterialModifier(ItemModifier):
    def __init__(self):
        super().__init__()
        self.permission_type = Modifier.ALL_PERMITTED_BUT_NOT_PROHIBITED
        self.permitted_entities = [Weapon, Armor]

    def apply_to(self, item):
        super().apply_to(item)

from erukar.engine.model import Modifier
from erukar.game.modifiers.base.ItemModifier import ItemModifier
from erukar.engine.inventory import Armor
from erukar.engine.inventory import Weapon

class MaterialModifier(ItemModifier):
    PermissionType = Modifier.ALL_PERMITTED_BUT_NOT_PROHIBITED
    PermittedEntities = [Weapon, Armor]

    def apply_to(self, item):
        item.material = self

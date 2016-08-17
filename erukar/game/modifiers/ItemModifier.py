from erukar.engine.model import Modifier
from erukar.engine.inventory import Item

class ItemModifier(Modifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Item]

    def apply_to(self, item):
        item.modifiers.append(self)

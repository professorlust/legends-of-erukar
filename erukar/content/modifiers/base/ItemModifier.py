from erukar.system.engine import Modifier, Item

class ItemModifier(Modifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Item]

    def apply_to(self, item):
        super().apply_to(item)
        item.modifiers.append(self)

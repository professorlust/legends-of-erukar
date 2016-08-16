from erukar.engine.model import Modifier
from erukar.engine.inventory import Item

class ItemModifier(Modifier):
    def __init__(self):
        super().__init__()
        self.permission_type = Modifier.ALL_PERMITTED
        self.permitted_entities = [Item]

    def apply_to(self, item):
        item.modifiers.append(self)

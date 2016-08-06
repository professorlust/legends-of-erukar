from erukar.engine.model import Modifier
from erukar.engine.inventory import Armor
from erukar.engine.inventory import Weapon

class MaterialModifier(Modifier):
    def __init__(self):
        super().__init__()
        self.permission_type = Modifier.ALL_PERMITTED
        self.permitted_entities.append(Weapon)
        self.permitted_entities.append(Armor)

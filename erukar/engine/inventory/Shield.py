from erukar.engine.inventory.Armor import Armor

class Shield(Armor):
    EssentialPart = "shield"
    EquipmentLocations = ['right','left']

    def __init__(self, name, modifiers=None):
        super().__init__(name, modifiers=modifiers)

from .Armor import Armor

class Shield(Armor):
    EssentialPart = "shield"
    EquipmentLocations = ['right','left']

    def __init__(self, modifiers=None):
        super().__init__(self.BaseName, modifiers=modifiers)

from erukar.engine.inventory.Armor import Armor

class Shield(Armor):
    EssentialPart = "shield"
    EquipmentLocations = ['right','left']

    def __init__(self, name):
        super().__init__(name)

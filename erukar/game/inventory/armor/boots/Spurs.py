from erukar.engine.inventory.Armor import Armor

class Spurs(Armor):
    EquipmentLocations = ['feet']
    BaseName="Spurs"
    Probability = 1

    def __init__(self):
        super().__init__("Spurs")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20



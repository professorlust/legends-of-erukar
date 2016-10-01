from erukar.engine.inventory.Armor import Armor

class Sabatons(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sabatons"
    Probability = 1

    def __init__(self):
        super().__init__("Sabatons")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


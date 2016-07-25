from erukar.engine.inventory.ArmArmor import ArmArmor

class Brace(ArmArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Brace")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20

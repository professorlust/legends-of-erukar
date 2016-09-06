from erukar.engine.inventory.ArmArmor import ArmArmor

class Vambrace(ArmArmor):
    BaseName="Vambrace"
    Probability = 1

    def __init__(self):
        super().__init__("Vambrace")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20

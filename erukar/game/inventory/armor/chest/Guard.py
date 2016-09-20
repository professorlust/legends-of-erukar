from erukar.engine.inventory.ChestArmor import ChestArmor

class Guard(ChestArmor):
    BaseName="Guard"
    Probability = 1

    def __init__(self):
        super().__init__("Guard")
        self.armor_class_modifier = 8
        self.max_dex_mod = 20

from erukar.engine.inventory.Shield import Shield

class RoundShield(Shield):
    Probability = 2

    def __init__(self):
        super().__init__("Round Shield")
        self.armor_class_modifier = 2
        self.max_dex_mod = 4


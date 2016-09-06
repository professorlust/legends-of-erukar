from erukar.engine.inventory.Shield import Shield

class ScutumShield(Shield):
    BaseName="Scutum Shield"
    Probability = 1

    def __init__(self):
        super().__init__("Scutum Shield")
        self.armor_class_modifier = 5
        self.max_dex_mod = 0


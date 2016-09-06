from erukar.engine.inventory.Shield import Shield

class KiteShield(Shield):
    BaseName="Kite Shield"
    Probability = 1

    def __init__(self):
        super().__init__("Kite Shield")
        self.armor_class_modifier = 4
        self.max_dex_mod = 1 

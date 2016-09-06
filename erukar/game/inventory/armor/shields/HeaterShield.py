from erukar.engine.inventory.Shield import Shield

class HeaterShield(Shield):
    BaseName="Heater Shield"
    Probability = 1

    def __init__(self):
        super().__init__("Heater Shield")
        self.armor_class_modifier = 3
        self.max_dex_mod = 3

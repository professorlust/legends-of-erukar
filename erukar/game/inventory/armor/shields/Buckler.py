from erukar.engine.inventory.Shield import Shield

class Buckler(Shield):
    BaseName="Buckler"
    Probability = 2

    def __init__(self):
        super().__init__("Buckler")
        self.armor_class_modifier = 1
        self.max_dex_mod = 5


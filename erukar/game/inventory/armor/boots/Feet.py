from erukar.engine.inventory.FootArmor import FootArmor

class Feet(FootArmor):
    '''Note: This requires a magical modifier!'''
    Probability = 1

    def __init__(self):
        super().__init__("Feet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20

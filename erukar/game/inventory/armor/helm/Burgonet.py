from erukar.engine.inventory.HeadArmor import HeadArmor

class Burgonet(HeadArmor):
    BaseName="Burgonet"
    Probability = 1

    def __init__(self):
        super().__init__("Burgonet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20

from erukar.engine.inventory.Weapon import Weapon

class Halberd(Weapon):
    Probability = 1
    BaseName = "Halberd"

    def __init__(self):
        super().__init__(Halberd.BaseName)
        self.damage = '1d6'

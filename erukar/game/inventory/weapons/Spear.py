from erukar.engine.inventory.Weapon import Weapon

class Spear(Weapon):
    Probability = 1
    BaseName = "Spear"

    def __init__(self):
        super().__init__(Spear.BaseName)
        self.damage = '1d6'

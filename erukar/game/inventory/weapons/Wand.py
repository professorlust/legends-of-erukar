from erukar.engine.inventory.Weapon import Weapon

class Wand(Weapon):
    Probability = 1
    BaseName = "Wand"

    def __init__(self):
        super().__init__(Wand.BaseName)
        self.damage = '1d6'

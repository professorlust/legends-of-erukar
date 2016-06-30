from erukar.engine.inventory.Weapon import Weapon

class Bow(Weapon):
    Probability = 1
    BaseName = "Bow"

    def __init__(self):
        super().__init__(Bow.BaseName)
        self.damage = '1d6'

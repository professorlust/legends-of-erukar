from erukar.engine.inventory.Weapon import Weapon

class Mace(Weapon):
    Probability = 1
    BaseName = "Mace"

    def __init__(self):
        super().__init__(Mace.BaseName)
        self.damage = '1d6'

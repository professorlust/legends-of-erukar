from erukar.engine.inventory.Weapon import Weapon

class Axe(Weapon):
    Probability = 1
    BaseName = "Axe"

    def __init__(self):
        super().__init__(Axe.BaseName)
        self.damage = '1d6'

from erukar.engine.inventory.Weapon import Weapon

class Rapier(Weapon):
    Probability = 1
    BaseName = "Rapier"

    def __init__(self):
        super().__init__(Rapier.BaseName)
        self.damage = '1d6'

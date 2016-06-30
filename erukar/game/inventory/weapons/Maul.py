from erukar.engine.inventory.Weapon import Weapon

class Maul(Weapon):
    Probability = 1
    BaseName = "Maul"

    def __init__(self):
        super().__init__(Maul.BaseName)
        self.damage = '1d6'

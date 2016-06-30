from erukar.engine.inventory.Weapon import Weapon

class CrossBow(Weapon):
    Probability = 1
    BaseName = "CrossBow"

    def __init__(self):
        super().__init__(CrossBow.BaseName)
        self.damage = '1d6'

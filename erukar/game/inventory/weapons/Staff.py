from erukar.engine.inventory.Weapon import Weapon

class Staff(Weapon):
    Probability = 1
    BaseName = "Staff"

    def __init__(self):
        super().__init__(Staff.BaseName)
        self.damage = '1d6'

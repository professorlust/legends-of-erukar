from erukar.engine.inventory.Weapon import Weapon

class MorningStar(Weapon):
    Probability = 1
    BaseName = "MorningStar"

    def __init__(self):
        super().__init__(MorningStar.BaseName)
        self.damage = '1d6'

from erukar.engine.inventory.Armor import Armor

class Leggings(Armor):
    BaseName="Leggings"
    Probability = 1
    BaseWeight = 1.0

    def __init__(self):
        super().__init__("Leggings")
        self.equipment_locations = ['legs']

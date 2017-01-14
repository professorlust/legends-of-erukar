from erukar.engine.inventory.Armor import Armor

class Guard(Armor):
    EquipmentLocations = ['chest']
    BaseName="Guard"
    Probability = 1
    BaseWeight = 5.0

    def __init__(self):
        super().__init__("Guard")

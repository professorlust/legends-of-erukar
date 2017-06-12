from erukar.engine.inventory.Armor import Armor

class Plate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Plate"
    Probability = 1

    InventoryDescription = "A full chest plate is capable of mitigating or glancing most blows, but is cumbersome to wear"
    BasePrice = 200
    BaseWeight = 9.7


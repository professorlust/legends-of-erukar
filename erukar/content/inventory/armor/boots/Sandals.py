from erukar.system.engine import Armor

class Sandals(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sandals"
    Probability = 1

    InventoryDescription = "Rudimentary shoe which is very light but offers little to no protection."
    BaseWeight = 0.5
    BasePrice = 15

    ArmorClass = Armor.Light
    DamageMitigations = {
        'bludgeoning': (0.05, 2),
        'piercing': (0.05, 2)
    }

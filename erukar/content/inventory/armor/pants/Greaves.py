from erukar.system.engine import Armor

class Greaves(Armor):
    EquipmentLocations = ['legs']
    BaseName="Greaves"
    Probability = 1

    InventoryDescription = "Greaves are part of a plate set but are often interchanged with Legplates."
    ArmorClass = Armor.Heavy
    BasePrice = 240
    BaseWeight = 20
    DamageMitigations = {
        'slashing': (0.30, 18),
        'piercing': (0.20, 12),
        'bludgeoning': (0.10, 6)
    }

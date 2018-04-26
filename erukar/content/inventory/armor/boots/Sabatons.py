from erukar.system.engine import Armor

class Sabatons(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sabatons"
    Probability = 1

    InventoryDescription = "Highly protective, armored footgear which is often part of a platemail suit. Provides a large amount of protection around all sides of the feet."
    BasePrice = 200
    BaseWeight = 8.0

    ArmorClass = Armor.Light
    EvasionPenalty = 0.15
    MovementSpeedPenalty = 0.10
    DamageMitigations = {
        'bludgeoning': (0.12, 6),
        'piercing': (0.15, 6),
        'slashing': (0.15, 6),
    }

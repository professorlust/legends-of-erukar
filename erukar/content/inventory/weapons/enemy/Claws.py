from erukar.system.engine.inventory import MartialWeapon


class Claws(MartialWeapon):
    IsInteractible = False
    Probability = 0
    BaseName = "Claws"
    EssentialPart = "points"
    CannotDrop = True
    AttackRange = 1

    SlashingPercentage = 0.5
    PiercingPercentage = 0.35
    BludgeoningPercentage = 0.15

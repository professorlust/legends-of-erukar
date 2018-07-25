from .Item import Item


class Armor(Item):
    Light = "LIGHT"
    Medium = "MEDIUM"
    Heavy = "HEAVY"

    EquipmentLocations = ['chest']
    Persistent = True
    EssentialPart = "armor"

    EvasionPenalty = 0.00
    AttackPenalty = 0.00
    MovementSpeedPenalty = 0.00
    VisionPenalty = 0.00

    ArmorClass = "error"
    DamageMitigations = {
        # type, mitigation percent, glancing range
        'bludgeoning': (0.05, 2),
        'piercing': (0.1, 4)
    }

    def __init__(self, name="", modifiers=None):
        super().__init__("armor", name or self.BaseName, modifiers=modifiers)

    def protection(self, damage_type):
        yield (0, 0)
        if self.durability <= 0.0:
            return
        yield from self.base_protection(damage_type)
        mod_methodname = '{}_protection'.format(damage_type)
        for modifier in self.modifiers:
            if hasattr(modifier, mod_methodname):
                yield getattr(modifier, mod_methodname)(self)

    def total_protection(self, damage_type):
        total = list(self.protection(damage_type))
        return tuple(sum(v) for v in zip(*total))

    def base_protection(self, damage_type):
        if damage_type in self.DamageMitigations:
            yield self.DamageMitigations[damage_type]

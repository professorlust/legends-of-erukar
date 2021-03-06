from erukar.system.engine import Condition, Weapon
import erukar

class AugmentedWeapon(Condition):
    IsTemporary = True
    Duration = 12 # In ticks, where a tick is 5 seconds
    Incapacitates = False
    MaxInstances = 1

    Noun = 'Augmented Weapon'
    Participle = 'Augmenting Weapon'
    Description = 'Adds a temporary effect to one or multiple weapons'

    def __init__(self, target, modifier_type, subclass):
        super().__init__(target)
        self.modifier_type = getattr(erukar.content.modifiers.inventory, modifier_type)
        self.timer = AugmentedWeapon.Duration
        self.weapon = None
        self.subclass = subclass
        self.modifier_instances = []
        self.augment_weapon(target)

    def name(self):
        return self.modifier_instances[0].on_alias('Weapon')

    def describe(self):
        return self.modifier_instances[0].InventoryDescription

    def tick(self):
        '''Countdown'''
        if self.IsTemporary:
            self.timer -= 1
            if self.timer <= 0:
                self.exit()

    def augment_weapon(self, target):
        '''Augment up to {MaxInstances} weapons, then track them so they can be removed later'''
        for slot in target.attack_slots:
            self.weapon = getattr(target, slot)
            if self.weapon is not None and isinstance(self.weapon, Weapon):
                modifier = self.modifier_type()
                modifier.apply_subclass(self.subclass)
                modifier.persistent = False
                modifier.apply_to(self.weapon)
                self.modifier_instances.append(modifier)
                if len(self.modifier_instances) >= self.MaxInstances:
                    return

    def exit(self):
        '''Remove all modifiers'''
        for modifier in self.modifier_instances:
            modifier.remove()
        self.target.conditions.remove(self)
